#!/bin/bash

# PR-Insight Web Interface Deployment Script

echo "🚀 Starting PR-Insight Web Interface Setup..."

# Check if we're in the web directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the web directory"
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building application..."
npm run build

echo "✅ Build completed successfully!"

echo ""
echo "🌐 To run locally:"
echo "  npm run dev"
echo ""
echo "📤 To deploy to Vercel:"
echo "  1. Install Vercel CLI: npm i -g vercel"
echo "  2. Login: vercel login"
echo "  3. Deploy: vercel --prod"
echo ""
echo "⚙️  Environment Variables needed in Vercel:"
echo "  - NEXT_PUBLIC_API_URL (your FastAPI backend URL)"
echo ""
echo "📚 For more information, see the README.md file"
