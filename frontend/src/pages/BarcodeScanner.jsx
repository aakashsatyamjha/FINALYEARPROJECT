import React, { useState, useEffect, useRef } from 'react';
import { Barcode, Camera, Search, Loader2, Upload, FileText, CheckCircle2, RefreshCw, AlertCircle } from 'lucide-react';
import { Html5Qrcode, Html5QrcodeSupportedFormats } from 'html5-qrcode';

const READER_ID = 'qr-reader-container';

const SAMPLE_PRODUCTS = [
  { barcode: '8901058921090', name: 'Parle Candy (Erythrosine INS 127)', brand: 'Parle', risk: 'Red Alert (US FDA Revoked, India OK)' },
  { barcode: '7622210817014', name: 'Oreo Cookies (Titanium Dioxide INS 171)', brand: 'Mondelez', risk: 'Red Alert (EU Banned, India/US OK)' },
  { barcode: '8901764123456', name: 'Britannia Bread (Azodicarbonamide INS 927a)', brand: 'Britannia', risk: 'Red Alert (EU Banned)' },
  { barcode: '8906127550010', name: 'Natural Peanut Butter Crunch', brand: 'Alpino', risk: 'All Countries OK (Clean)' },
  { barcode: '8901262010047', name: 'Amul Pure Cow Ghee', brand: 'Amul', risk: 'All Countries OK (Clean)' },
  { barcode: '8901058852813', name: 'Maggi 2-Min Masala Noodles (MSG INS 621)', brand: 'Nestlé', risk: 'Moderate Risk' },
];

const SAMPLE_INGREDIENT_LISTS = [
  { title: "Standard Biscuit", text: "Wheat flour, Sugar, Palm oil, Milk solids, Salt, INS 500(ii), INS 503(ii), Vanilla flavour" },
  { title: "Instant Noodles", text: "Refined wheat flour, Palm oil, Salt, Wheat gluten, INS 508, INS 412, INS 501i, INS 621, INS 150d" },
  { title: "Banned Dye / Titanium Dioxide", text: "Sugar, Palm oil, Titanium Dioxide (INS 171), Sodium Benzoate (INS 211), Citric acid" },
  { title: "Erythrosine & Potassium Bromate", text: "Wheat flour, Sugar, Potassium Bromate (INS 924a), Erythrosine (INS 127)" },
];

export default function BarcodeScanner({ onScanSuccess, onAnalyzeIngredients, onAnalyzeImage, loading, error }) {
  const [activeTab, setActiveTab] = useState('barcode'); // 'barcode' | 'ingredient'
  const [barcodeInput, setBarcodeInput] = useState('');
  
  // Ingredient Tab modes: 'text' | 'camera' | 'image'
  const [ingredientMode, setIngredientMode] = useState('text');
  const [ingredientText, setIngredientText] = useState('');
  const [productNameInput, setProductNameInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  // Barcode Camera scanner states
  const [barcodeScannerState, setBarcodeScannerState] = useState('idle'); // 'idle' | 'starting' | 'active' | 'error'
  const [barcodeCameraError, setBarcodeCameraError] = useState(null);
  const html5QrRef = useRef(null);

  // Label Photo Camera capture states
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [labelCameraActive, setLabelCameraActive] = useState(false);
  const [labelCameraError, setLabelCameraError] = useState(null);
  const mediaStreamRef = useRef(null);

  // Cleanup on unmount & revoke blob URLs to avoid memory leaks
  useEffect(() => {
    return () => {
      stopBarcodeScanner();
      stopLabelCamera();
      if (previewUrl) {
        try { URL.revokeObjectURL(previewUrl); } catch (_) {}
      }
    };
  }, [previewUrl]);

  // When switching ingredient mode to camera, start stream automatically
  useEffect(() => {
    if (ingredientMode === 'camera' && activeTab === 'ingredient') {
      startLabelCamera();
    } else {
      stopLabelCamera();
    }
  }, [ingredientMode, activeTab]);

  // ─────────────────────────────────────────────────────────────
  // 1. BARCODE CAMERA SCANNER FUNCTIONS (SAFE FROM REACT CRASH)
  // ─────────────────────────────────────────────────────────────
  const stopBarcodeScanner = async () => {
    setBarcodeScannerState('idle');
    if (!html5QrRef.current) return;
    try {
      const state = html5QrRef.current.getState?.();
      if (state === 2) {
        await html5QrRef.current.stop();
      }
      html5QrRef.current.clear?.();
    } catch (_) {}
    html5QrRef.current = null;
  };

  const startBarcodeScanner = async () => {
    // Prevent race conditions on rapid clicking
    if (barcodeScannerState === 'starting' || barcodeScannerState === 'active') return;

    setBarcodeCameraError(null);
    setBarcodeScannerState('starting');
    await stopBarcodeScanner();

    // Verify browser support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setBarcodeCameraError('Camera access is not supported in this browser environment. Please use manual barcode entry.');
      setBarcodeScannerState('error');
      return;
    }

    try {
      const formatsToSupport = [
        Html5QrcodeSupportedFormats.EAN_13,
        Html5QrcodeSupportedFormats.EAN_8,
        Html5QrcodeSupportedFormats.UPC_A,
        Html5QrcodeSupportedFormats.UPC_E,
        Html5QrcodeSupportedFormats.CODE_128,
        Html5QrcodeSupportedFormats.CODE_39,
        Html5QrcodeSupportedFormats.QR_CODE,
      ];

      const instance = new Html5Qrcode(READER_ID, { formatsToSupport, verbose: false });
      html5QrRef.current = instance;

      await instance.start(
        { facingMode: 'environment' },
        { fps: 10, qrbox: { width: 250, height: 160 }, aspectRatio: 1.5 },
        (decodedText) => {
          stopBarcodeScanner().then(() => onScanSuccess(decodedText));
        },
        () => {}
      );
      setBarcodeScannerState('active');
    } catch (err) {
      html5QrRef.current = null;
      console.warn("Barcode camera notice:", err);
      setBarcodeCameraError(
        'Camera permission was not granted or device camera is in use. You can type the barcode number below.'
      );
      setBarcodeScannerState('error');
    }
  };

  const handleBarcodeSubmit = (e) => {
    e.preventDefault();
    const trimmed = barcodeInput.trim();
    if (!trimmed) return;
    onScanSuccess(trimmed);
  };

  // ─────────────────────────────────────────────────────────────
  // 2. INGREDIENT LABEL PHOTO CAMERA SNAPSHOT FUNCTIONS
  // ─────────────────────────────────────────────────────────────
  const startLabelCamera = async () => {
    setLabelCameraError(null);
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera device API is not supported in this browser.');
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
      });
      mediaStreamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        try {
          await videoRef.current.play();
        } catch (_) {}
      }
      setLabelCameraActive(true);
    } catch (err) {
      console.warn("Label camera notice:", err);
      setLabelCameraError(
        'Camera unavailable (' + (err.message || 'permission required') + '). Please use "Upload Label File" to select an image.'
      );
      setLabelCameraActive(false);
    }
  };

  const stopLabelCamera = () => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => {
        try { track.stop(); } catch (_) {}
      });
      mediaStreamRef.current = null;
    }
    setLabelCameraActive(false);
  };

  const captureLabelSnapshot = (e) => {
    if (e && e.preventDefault) e.preventDefault();
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    // Ensure video stream has loaded valid frames
    if (video.readyState < 2) {
      setLabelCameraError("Camera is currently initializing. Please wait a second and try capturing again.");
      return;
    }

    const w = video.videoWidth || 640;
    const h = video.videoHeight || 480;
    canvas.width = w;
    canvas.height = h;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, w, h);

    canvas.toBlob((blob) => {
      if (blob) {
        if (previewUrl) {
          try { URL.revokeObjectURL(previewUrl); } catch (_) {}
        }
        const file = new File([blob], `label_photo_${Date.now()}.jpg`, { type: 'image/jpeg' });
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
        stopLabelCamera();
      }
    }, 'image/jpeg', 0.92);
  };

  // ─────────────────────────────────────────────────────────────
  // 3. INGREDIENT SUBMIT HANDLER
  // ─────────────────────────────────────────────────────────────
  const handleIngredientSubmit = (e) => {
    e.preventDefault();
    if (ingredientMode === 'text') {
      const trimmed = ingredientText.trim();
      if (!trimmed) return;
      if (onAnalyzeIngredients) {
        onAnalyzeIngredients(trimmed, productNameInput.trim() || "Custom Food Product");
      }
    } else {
      if (!selectedFile) return;
      if (onAnalyzeImage) {
        onAnalyzeImage(selectedFile);
      }
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (previewUrl) {
        try { URL.revokeObjectURL(previewUrl); } catch (_) {}
      }
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* ── Page Header ── */}
      <div className="space-y-1">
        <h1 className="text-xl font-bold text-gray-900">Check Your Product</h1>
        <p className="text-xs text-gray-600">
          Choose a method below to check product safety and regulations against the 300-record dataset.
        </p>
      </div>

      {/* ── Method Selector Tabs ── */}
      <div className="flex items-center gap-2 border-b border-gray-200 pb-3">
        <button
          onClick={() => { setActiveTab('barcode'); stopBarcodeScanner(); stopLabelCamera(); }}
          className={`px-4 py-2 rounded-md text-xs font-semibold transition-colors flex items-center gap-2 cursor-pointer ${
            activeTab === 'barcode'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
          }`}
        >
          <Barcode className="w-4 h-4" />
          <span>Scan Barcode</span>
        </button>

        <button
          onClick={() => { setActiveTab('ingredient'); stopBarcodeScanner(); }}
          className={`px-4 py-2 rounded-md text-xs font-semibold transition-colors flex items-center gap-2 cursor-pointer ${
            activeTab === 'ingredient'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Check Ingredients (Text / Camera / Image)</span>
        </button>
      </div>

      {/* ── Global Error Notice ── */}
      {error && (
        <div className="p-3.5 rounded bg-red-50 border border-red-200 text-xs text-red-800 space-y-1">
          <strong className="block font-bold">Product Lookup Notice</strong>
          <p>{error}</p>
        </div>
      )}

      {/* ── Method 1: BARCODE SCANNER ── */}
      {activeTab === 'barcode' && (
        <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-6">
          
          {/* Camera Scanner Box */}
          <div className="space-y-3">
            <h2 className="text-sm font-bold text-gray-900 flex items-center gap-2">
              <Camera className="w-4 h-4 text-gray-600" />
              <span>Camera Scanner (1D EAN-13 / UPC Barcodes)</span>
            </h2>

            {/* SAFE WRAPPER: READER_ID has ZERO React children so Html5Qrcode cannot crash React */}
            <div className="relative w-full bg-gray-900 rounded border border-gray-300 min-h-[220px] flex items-center justify-center text-white text-xs overflow-hidden">
              <div id={READER_ID} className="w-full h-full min-h-[220px]" />

              {barcodeScannerState === 'idle' && (
                <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-4 bg-gray-900 z-10 pointer-events-none">
                  <Camera className="w-8 h-8 text-gray-400 mb-2" />
                  <p className="font-semibold text-gray-200">Camera scanner ready</p>
                  <p className="text-[11px] text-gray-400 mt-1">Click button below to enable camera</p>
                </div>
              )}

              {barcodeScannerState === 'starting' && (
                <div className="absolute inset-0 flex items-center justify-center bg-gray-900/90 z-10 text-xs text-gray-300">
                  <Loader2 className="w-5 h-5 animate-spin mr-2 text-blue-500" />
                  <span>Connecting to camera hardware...</span>
                </div>
              )}
            </div>

            {barcodeCameraError && (
              <div className="text-xs text-amber-800 bg-amber-50 p-2.5 rounded border border-amber-200 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <p>{barcodeCameraError}</p>
              </div>
            )}

            {barcodeScannerState === 'idle' || barcodeScannerState === 'error' ? (
              <button
                type="button"
                onClick={startBarcodeScanner}
                disabled={loading}
                className="w-full py-2.5 px-4 rounded bg-gray-900 hover:bg-gray-800 text-white text-xs font-semibold cursor-pointer"
              >
                Enable Camera Scanner
              </button>
            ) : (
              <button
                type="button"
                onClick={stopBarcodeScanner}
                className="w-full py-2.5 px-4 rounded bg-red-600 hover:bg-red-700 text-white text-xs font-semibold cursor-pointer"
              >
                Stop Camera
              </button>
            )}
          </div>

          {/* Manual Entry */}
          <div className="border-t border-gray-100 pt-4 space-y-3">
            <h2 className="text-sm font-bold text-gray-900">
              Manual Barcode Entry
            </h2>

            <form onSubmit={handleBarcodeSubmit} className="space-y-3">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700 block">
                  Barcode Number:
                </label>
                <input
                  type="text"
                  value={barcodeInput}
                  onChange={(e) => setBarcodeInput(e.target.value)}
                  placeholder="e.g. 8901262010047"
                  className="w-full px-3 py-2 border border-gray-300 rounded text-sm text-gray-900 font-mono focus:outline-none focus:border-blue-600"
                />
              </div>

              <button
                type="submit"
                disabled={loading || !barcodeInput.trim()}
                className="w-full py-2.5 px-4 rounded bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <span>Check Product</span>
                )}
              </button>
            </form>
          </div>

          {/* Sample Barcodes */}
          <div className="border-t border-gray-100 pt-4 space-y-2">
            <h3 className="text-xs font-bold text-gray-700">
              Or Click a Sample Product to Test:
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {SAMPLE_PRODUCTS.map((p) => (
                <button
                  key={p.barcode}
                  onClick={() => { setBarcodeInput(p.barcode); onScanSuccess(p.barcode); }}
                  disabled={loading}
                  className="p-2.5 rounded border border-gray-200 hover:border-blue-500 hover:bg-blue-50 text-left transition-colors text-xs flex items-center justify-between cursor-pointer"
                >
                  <div>
                    <strong className="text-gray-900 block">{p.name}</strong>
                    <span className="text-gray-500 font-mono text-[11px]">{p.barcode}</span>
                  </div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ml-2 shrink-0 ${
                    p.risk.includes('Red Alert') ? 'bg-red-50 text-red-700 border-red-200' :
                    p.risk.includes('Moderate') ? 'bg-amber-50 text-amber-700 border-amber-200' :
                    'bg-green-50 text-green-700 border-green-200'
                  }`}>
                    {p.risk}
                  </span>
                </button>
              ))}
            </div>
          </div>

        </div>
      )}

      {/* ── Method 2: INGREDIENT ANALYSIS (TEXT / CAMERA SNAPSHOT / FILE UPLOAD) ── */}
      {activeTab === 'ingredient' && (
        <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-5">
          
          {/* Sub-mode selector tabs */}
          <div className="flex items-center gap-3 border-b border-gray-100 pb-2 flex-wrap">
            <button
              type="button"
              onClick={() => { setIngredientMode('text'); }}
              className={`text-xs font-bold pb-1 border-b-2 transition-colors cursor-pointer ${
                ingredientMode === 'text'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Type Comma-Separated Ingredients
            </button>

            <button
              type="button"
              onClick={() => { setIngredientMode('camera'); }}
              className={`text-xs font-bold pb-1 border-b-2 transition-colors cursor-pointer flex items-center gap-1 ${
                ingredientMode === 'camera'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Camera className="w-3.5 h-3.5" />
              <span>Capture Photo via Camera</span>
            </button>

            <button
              type="button"
              onClick={() => { setIngredientMode('image'); }}
              className={`text-xs font-bold pb-1 border-b-2 transition-colors cursor-pointer ${
                ingredientMode === 'image'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Upload Label File
            </button>
          </div>

          <form onSubmit={handleIngredientSubmit} className="space-y-4">
            
            {/* Product Name (Optional) */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-gray-700 block">
                Product Name (Optional):
              </label>
              <input
                type="text"
                value={productNameInput}
                onChange={(e) => setProductNameInput(e.target.value)}
                placeholder="e.g. Potato Chips, Tomato Ketchup, Biscuits"
                className="w-full px-3 py-2 border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:border-blue-600"
              />
            </div>

            {/* Mode 1: Comma Separated Textarea */}
            {ingredientMode === 'text' && (
              <div className="space-y-3">
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-gray-700 block">
                    Enter Ingredients (comma separated):
                  </label>
                  <textarea
                    rows={4}
                    value={ingredientText}
                    onChange={(e) => setIngredientText(e.target.value)}
                    placeholder="e.g. Wheat flour, Sugar, Palm oil, Sodium benzoate, INS 500(ii), Tartrazine"
                    className="w-full px-3 py-2 border border-gray-300 rounded text-xs text-gray-900 focus:outline-none focus:border-blue-600 leading-relaxed font-sans"
                  />
                </div>

                {/* Preset Ingredient Examples */}
                <div className="space-y-1.5 pt-1">
                  <span className="text-[11px] font-semibold text-gray-500 block">
                    Click a sample ingredient list to test:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {SAMPLE_INGREDIENT_LISTS.map((sample, i) => (
                      <button
                        key={i}
                        type="button"
                        onClick={() => {
                          setIngredientText(sample.text);
                          setProductNameInput(sample.title);
                        }}
                        className="px-2.5 py-1 rounded bg-gray-100 hover:bg-gray-200 border border-gray-200 text-gray-700 text-[11px] font-medium transition-colors"
                      >
                        + {sample.title}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Mode 2: Camera Photo Capture */}
            {ingredientMode === 'camera' && (
              <div className="space-y-3">
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-gray-700 block">
                    Align ingredient label in camera viewfinder:
                  </label>

                  <div className="relative w-full bg-gray-900 rounded border border-gray-300 min-h-[220px] flex items-center justify-center text-white text-xs overflow-hidden">
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className={`w-full max-h-64 object-contain ${labelCameraActive ? 'block' : 'hidden'}`}
                    />
                    
                    {!labelCameraActive && !previewUrl && (
                      <div className="text-center space-y-2 p-4 text-gray-300">
                        <Camera className="w-8 h-8 mx-auto text-gray-400" />
                        <p className="font-semibold">Starting camera viewfinder...</p>
                      </div>
                    )}
                    
                    {previewUrl && !labelCameraActive && (
                      <img src={previewUrl} alt="Captured Label" className="max-h-64 object-contain" />
                    )}
                  </div>
                  <canvas ref={canvasRef} className="hidden" />
                </div>

                {labelCameraError && (
                  <div className="text-xs text-amber-800 bg-amber-50 p-2.5 rounded border border-amber-200 flex items-start gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    <p>{labelCameraError}</p>
                  </div>
                )}

                <div className="flex gap-2">
                  {labelCameraActive ? (
                    <button
                      type="button"
                      onClick={captureLabelSnapshot}
                      className="flex-1 py-2.5 px-4 rounded bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs cursor-pointer flex items-center justify-center gap-2"
                    >
                      <Camera className="w-4 h-4" />
                      <span>📸 Capture Photo</span>
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={startLabelCamera}
                      className="flex-1 py-2 px-4 rounded bg-gray-800 hover:bg-gray-900 text-white font-semibold text-xs cursor-pointer flex items-center justify-center gap-2"
                    >
                      <RefreshCw className="w-3.5 h-3.5" />
                      <span>Retake Photo</span>
                    </button>
                  )}
                </div>

                {previewUrl && (
                  <p className="text-[11px] text-green-700 font-semibold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Photo captured! Click "Analyze Ingredients" below to run PaddleOCR extraction.</span>
                  </p>
                )}
              </div>
            )}

            {/* Mode 3: Label Image File Upload */}
            {ingredientMode === 'image' && (
              <div className="space-y-3">
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center space-y-3 bg-gray-50">
                  <Upload className="w-8 h-8 text-gray-400 mx-auto" />
                  <div>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileChange}
                      className="hidden"
                      id="ingredient-image-input"
                    />
                    <label
                      htmlFor="ingredient-image-input"
                      className="px-4 py-2 rounded bg-white border border-gray-300 text-gray-700 text-xs font-semibold cursor-pointer hover:bg-gray-50 inline-block"
                    >
                      Choose Image File
                    </label>
                  </div>
                  {selectedFile && (
                    <p className="text-xs text-gray-600 font-mono">{selectedFile.name}</p>
                  )}
                </div>

                {previewUrl && (
                  <div className="space-y-1">
                    <span className="text-xs font-semibold text-gray-700 block">Preview</span>
                    <div className="max-h-48 rounded border border-gray-200 overflow-hidden bg-gray-100 flex items-center justify-center">
                      <img src={previewUrl} alt="Ingredient Preview" className="max-h-48 object-contain" />
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || (ingredientMode === 'text' ? !ingredientText.trim() : !selectedFile)}
              className="w-full py-2.5 px-4 rounded bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Extracting & Analyzing OCR...</span>
                </>
              ) : (
                <span>Analyze Ingredients</span>
              )}
            </button>
          </form>

        </div>
      )}

    </div>
  );
}
