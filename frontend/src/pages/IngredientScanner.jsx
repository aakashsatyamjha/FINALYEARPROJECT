import React, { useState, useRef, useEffect, useCallback } from 'react';
import { 
  Camera, 
  Upload, 
  FileText, 
  Loader2, 
  RefreshCw, 
  CheckCircle2, 
  Zap, 
  Send, 
  X, 
  Image as ImageIcon,
  AlertCircle,
  Sparkles,
  Edit3
} from 'lucide-react';
import { createWorker } from 'tesseract.js';

const PRESETS = [
  { 
    label: 'Adulterated Turmeric (Metanil Yellow + Lead Chromate)', 
    name: 'Turmeric Powder Sample',
    brand: 'Suspect Brand',
    category: 'Spices',
    text: 'Ingredients: Pure Turmeric powder (Curcuma longa), Metanil Yellow industrial dye, Lead Chromate yellow pigment, bulk starch filler.' 
  },
  { 
    label: 'Maggi 2-Minute Noodles (Commercial Formulation)', 
    name: 'Maggi 2-Minute Noodles',
    brand: 'Nestlé',
    category: 'Instant Noodles',
    text: 'Ingredients: Wheat Flour (Maida), Palm Oil, Salt, Wheat Gluten, Mineral (Calcium Carbonate), Guar Gum. Tastemaker: Mixed Spices (Onion Powder, Coriander, Turmeric, Cumin), Sugar, Salt, Hydrolysed Groundnut Protein, Flavour Enhancer (INS 635), Acidity Regulator (INS 330).' 
  },
  { 
    label: 'Fresh Pasteurised Toned Milk (Pure Dairy)', 
    name: 'Amul Taaza Toned Milk',
    brand: 'Amul',
    category: 'Dairy',
    text: 'Ingredients: Pasteurised Toned Milk, Vitamin A, Vitamin D2. Fat 3.0% minimum, Solids Not Fat (SNF) 8.5% minimum. No added preservatives, zero adulterants.' 
  },
];

const CATEGORIES = [
  'Packaged Food',
  'Instant Noodles',
  'Biscuits & Bakery',
  'Dairy Products',
  'Spices & Condiments',
  'Beverages & Soft Drinks',
  'Extruded & Fried Snacks',
  'Confectionery & Sweets',
  'Cooking Oils & Ghee'
];

export default function IngredientScanner({ onAnalyze, loading }) {
  const [mode, setMode] = useState('camera'); // 'camera' | 'upload'
  const [stream, setStream] = useState(null);
  const [cameraReady, setCameraReady] = useState(false);
  const [cameraError, setCameraError] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  
  const [ocrStatus, setOcrStatus] = useState('idle'); // 'idle' | 'processing' | 'done' | 'notext' | 'error'
  const [ocrProgress, setOcrProgress] = useState(0);
  const [ocrError, setOcrError] = useState(null);
  
  const [extractedText, setExtractedText] = useState('');
  const [productName, setProductName] = useState('');
  const [brand, setBrand] = useState('');
  const [category, setCategory] = useState('Packaged Food');

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);
  const cameraFileRef = useRef(null);

  // Initialize camera stream
  const startCamera = useCallback(async () => {
    setCameraReady(false);
    setCameraError(null);
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const newStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
        });
        setStream(newStream);
        if (videoRef.current) {
          videoRef.current.srcObject = newStream;
        }
      } else {
        setCameraError('Camera API is not available in this browser. Use the Upload tab instead.');
      }
    } catch (err) {
      console.warn("Camera initialization notice:", err);
      setCameraError(
        err.name === 'NotAllowedError'
          ? 'Camera access was denied. Please allow camera permission in your browser settings, or use the Upload tab.'
          : err.name === 'NotFoundError'
            ? 'No camera found on this device. Use the Upload tab or take a photo with your phone camera below.'
            : `Camera could not be started (${err.message}). Use the Upload tab instead.`
      );
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setCameraReady(false);
  }, [stream]);

  // Handle video element becoming ready to play
  const handleVideoCanPlay = useCallback(() => {
    if (videoRef.current) {
      const v = videoRef.current;
      if (v.videoWidth > 0 && v.videoHeight > 0) {
        setCameraReady(true);
        v.play().catch(() => {});
      }
    }
  }, []);

  useEffect(() => {
    if (mode === 'camera' && !imageSrc) {
      startCamera();
    } else {
      stopCamera();
    }
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [mode, imageSrc]);

  const captureImage = () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    
    // Guard: make sure the video has real pixel data
    if (!video.videoWidth || !video.videoHeight || video.videoWidth < 10) {
      setOcrError('Camera is not ready yet. Please wait a moment and try again.');
      return;
    }

    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const dataUrl = canvas.toDataURL('image/jpeg', 0.95);
    setImageSrc(dataUrl);

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], 'captured_label.jpg', { type: 'image/jpeg' });
        setImageFile(file);
        triggerOCR(dataUrl, file);
      }
    }, 'image/jpeg', 0.95);

    stopCamera();
  };

  // Handle file chosen from the regular upload input OR the camera capture input (mobile)
  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setImageFile(file);
    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target.result;
      setImageSrc(dataUrl);
      triggerOCR(dataUrl, file);
    };
    reader.readAsDataURL(file);
  };

  const triggerOCR = async (dataUrl, file) => {
    setOcrStatus('processing');
    setOcrProgress(5);
    setOcrError(null);

    try {
      // 1. Client-Side WebAssembly OCR using Tesseract.js
      const worker = await createWorker('eng', 1, {
        logger: (m) => {
          if (m.status === 'recognizing text') {
            const pct = Math.round(m.progress * 100);
            setOcrProgress(pct > 5 ? pct : 5);
          }
        }
      });

      const res = await worker.recognize(dataUrl);
      await worker.terminate();

      let text = res?.data?.text || '';
      text = text.replace(/\r\n/g, ' ').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();

      if (text.length < 5 && file) {
        // 2. Server-side OpenCV Fallback
        try {
          const formData = new FormData();
          formData.append('file', file);
          const srvRes = await fetch('/api/ocr/extract', {
            method: 'POST',
            body: formData,
          });
          if (srvRes.ok) {
            const srvData = await srvRes.json();
            const serverText = srvData.extracted_text || srvData.cleaned_text || srvData.raw_text || '';
            if (serverText && serverText.length > 5) {
              text = serverText;
            }
          }
        } catch (srvErr) {
          console.warn("Server OCR fallback notice:", srvErr);
        }
      }

      if (text && text.length > 5) {
        setExtractedText(text);
        setOcrStatus('done');
      } else {
        setExtractedText('');
        setOcrStatus('notext');
      }
    } catch (err) {
      console.error("OCR execution error:", err);
      setOcrError("Optical character recognition failed. You can type or paste the ingredient list manually.");
      setOcrStatus('error');
    }
  };

  const retakeImage = () => {
    setImageSrc(null);
    setImageFile(null);
    setExtractedText('');
    setOcrStatus('idle');
    setOcrProgress(0);
    setOcrError(null);
    setCameraError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (cameraFileRef.current) {
      cameraFileRef.current.value = '';
    }
    if (mode === 'camera') {
      startCamera();
    }
  };

  const applyPreset = (preset) => {
    setProductName(preset.name);
    setBrand(preset.brand);
    setCategory(preset.category);
    setExtractedText(preset.text);
    setOcrStatus('done');
  };

  const handleSubmitAnalysis = (e) => {
    e.preventDefault();
    if (!extractedText.trim()) return;

    onAnalyze({
      product_name: productName.trim() || 'Scanned Food Product',
      brand: brand.trim() || 'Packaged Goods',
      category: category || 'Packaged Food',
      ingredients: extractedText.trim(),
      scan_type: 'ocr'
    });
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      
      {/* Hidden Canvas for Snapshot */}
      <canvas ref={canvasRef} className="hidden" />

      {/* ── Header ── */}
      <div className="glass-card rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 bg-emerald-500/10 px-2.5 py-0.5 rounded-lg border border-emerald-500/20">
              Module 02
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-500 font-medium">Computer Vision & OCR</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Ingredient Label Scanner & OCR
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Capture a live camera photo or upload an image of any food ingredient label to extract text and analyze for adulterants.
          </p>
        </div>

        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 shrink-0">
          <button
            onClick={() => { setMode('camera'); retakeImage(); }}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
              mode === 'camera'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Camera className="w-3.5 h-3.5" />
            <span>Camera</span>
          </button>
          
          <button
            onClick={() => { setMode('upload'); retakeImage(); }}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
              mode === 'upload'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Upload Image</span>
          </button>
        </div>
      </div>

      {/* ── 2-Column Main Workspace ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Left Column (5 cols): Visual Capture Card */}
        <div className="lg:col-span-5 glass-card rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-bold text-slate-900 text-base">
              {mode === 'camera' ? 'Live Camera Capture' : 'Label Image Upload'}
            </h2>
            {imageSrc && (
              <button
                onClick={retakeImage}
                className="text-xs text-slate-600 hover:text-slate-900 font-semibold flex items-center gap-1 bg-slate-100 hover:bg-slate-200 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
              >
                <RefreshCw className="w-3 h-3" />
                <span>Retake</span>
              </button>
            )}
          </div>

          {/* Visual Container */}
          <div className="w-full rounded-2xl overflow-hidden bg-slate-950 border border-slate-200 relative aspect-4/3 flex items-center justify-center text-white">
            
            {/* 1. Live Camera Stream */}
            {mode === 'camera' && !imageSrc && !cameraError && (
              <>
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  onCanPlay={handleVideoCanPlay}
                  onLoadedMetadata={handleVideoCanPlay}
                  className="w-full h-full object-cover"
                />
                {cameraReady && (
                  <div className="absolute inset-0 border-2 border-dashed border-emerald-400/40 m-6 rounded-xl pointer-events-none flex items-center justify-center">
                    <span className="bg-slate-950/80 px-3 py-1 rounded-lg text-xs font-medium text-emerald-400 border border-emerald-500/30">
                      Align Ingredient Text Here
                    </span>
                  </div>
                )}
                {!cameraReady && (
                  <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/90 gap-2">
                    <Loader2 className="w-6 h-6 animate-spin text-emerald-400" />
                    <span className="text-xs text-slate-400">Initializing camera...</span>
                  </div>
                )}
              </>
            )}

            {/* 1b. Camera Error State */}
            {mode === 'camera' && !imageSrc && cameraError && (
              <div className="w-full h-full flex flex-col items-center justify-center p-6 text-center space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-amber-400">
                  <AlertCircle className="w-6 h-6" />
                </div>
                <p className="text-xs text-slate-400 max-w-[240px] leading-relaxed">{cameraError}</p>
                <button
                  type="button"
                  onClick={() => cameraFileRef.current?.click()}
                  className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs transition-colors flex items-center gap-1.5 cursor-pointer"
                >
                  <Camera className="w-3.5 h-3.5" />
                  <span>Take Photo with Device Camera</span>
                </button>
                <input
                  ref={cameraFileRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>
            )}

            {/* 2. Upload Dropzone */}
            {mode === 'upload' && !imageSrc && (
              <div 
                onClick={() => fileInputRef.current?.click()}
                className="w-full h-full flex flex-col items-center justify-center p-6 text-center space-y-2 cursor-pointer hover:bg-slate-900 transition-colors"
              >
                <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-400">
                  <ImageIcon className="w-6 h-6" />
                </div>
                <p className="text-sm font-semibold text-slate-200">
                  Click to select label image
                </p>
                <p className="text-xs text-slate-400">
                  PNG, JPG, or WEBP up to 10MB
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>
            )}

            {/* 3. Snapshot / Uploaded Image Preview */}
            {imageSrc && (
              <img
                src={imageSrc}
                alt="Captured Label"
                className="w-full h-full object-contain bg-slate-950"
              />
            )}

          </div>

          {/* Capture Controls */}
          {mode === 'camera' && !imageSrc && !cameraError && (
            <button
              onClick={captureImage}
              disabled={!cameraReady}
              className="w-full py-3 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-sm shadow-md shadow-emerald-600/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 cursor-pointer"
            >
              <Camera className="w-4 h-4" />
              <span>{cameraReady ? 'Capture Photo for OCR' : 'Waiting for camera...'}</span>
            </button>
          )}

          {mode === 'upload' && !imageSrc && (
            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full py-3 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-xs transition-colors flex items-center justify-center gap-2 cursor-pointer"
            >
              <Upload className="w-4 h-4" />
              <span>Browse Image File</span>
            </button>
          )}

          {/* OCR Processing State */}
          {ocrStatus === 'processing' && (
            <div className="p-3.5 rounded-xl bg-slate-100 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-1.5">
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-500" />
                  Extracting Text via Tesseract.js...
                </span>
                <span className="font-mono text-emerald-500">{ocrProgress}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-emerald-500 transition-all duration-300 rounded-full"
                  style={{ width: `${ocrProgress}%` }}
                />
              </div>
            </div>
          )}

          {ocrStatus === 'done' && (
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-xs text-emerald-600 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
              <span>Text extracted successfully. Please review formulation below.</span>
            </div>
          )}

          {ocrStatus === 'notext' && (
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/25 text-xs text-amber-600 flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
              <span>No readable text was detected in this image. Try again with better lighting, or type/paste the ingredient list manually in the text box.</span>
            </div>
          )}

          {ocrError && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/25 text-xs text-rose-400 flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
              <span>{ocrError}</span>
            </div>
          )}
        </div>

        {/* Right Column (7 cols): Extracted Text & Analysis Form */}
        <div className="lg:col-span-7 glass-card rounded-2xl p-6 space-y-5">
          <div>
            <h2 className="font-bold text-slate-900 text-base">
              Product Details & Ingredient Formulation
            </h2>
            <p className="text-xs text-slate-500">
              Review extracted text, correct typos if needed, and run the AI adulteration classifier.
            </p>
          </div>

          <form onSubmit={handleSubmitAnalysis} className="space-y-4">
            
            {/* Metadata Inputs (2 cols) */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Product Name
                </label>
                <input
                  type="text"
                  value={productName}
                  onChange={(e) => setProductName(e.target.value)}
                  placeholder="e.g. Masala Turmeric Powder"
                  className="w-full px-3 py-2 rounded-xl bg-slate-100 border border-slate-200 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 text-slate-900 text-sm outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Brand / Manufacturer
                </label>
                <input
                  type="text"
                  value={brand}
                  onChange={(e) => setBrand(e.target.value)}
                  placeholder="e.g. Everest / Local Spices"
                  className="w-full px-3 py-2 rounded-xl bg-slate-100 border border-slate-200 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 text-slate-900 text-sm outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Product Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-100 border border-slate-200 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 text-slate-900 text-sm outline-none cursor-pointer"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            {/* Extracted Ingredients Text Area */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
                  <Edit3 className="w-3.5 h-3.5 text-emerald-500" />
                  <span>Ingredient List (Extracted / Editable)</span>
                </label>
                <span className="text-[11px] text-slate-400 font-mono">
                  {extractedText.length} characters
                </span>
              </div>
              <textarea
                rows={5}
                value={extractedText}
                onChange={(e) => setExtractedText(e.target.value)}
                placeholder="Captured or typed ingredient formulation will appear here. For example: Wheat flour, palm oil, salt, disodium guanylate, Metanil Yellow..."
                className="w-full p-3 rounded-xl bg-slate-100 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-1 focus:ring-emerald-500 text-slate-900 text-xs font-mono leading-relaxed outline-none transition-colors"
              />
            </div>

            {/* Submit Action */}
            <button
              type="submit"
              disabled={loading || !extractedText.trim()}
              className="w-full py-3 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-sm shadow-md shadow-emerald-600/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 cursor-pointer"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Running AI Quality & Adulteration Screening...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Run AI Quality & Adulteration Analysis</span>
                </>
              )}
            </button>

          </form>

          {/* Quick Presets Bar */}
          <div className="pt-3 border-t border-slate-200 space-y-2">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
              Or Load Verified Benchmark Presets:
            </span>
            <div className="flex flex-wrap gap-2">
              {PRESETS.map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => applyPreset(p)}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium transition-colors border border-slate-200 cursor-pointer"
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
