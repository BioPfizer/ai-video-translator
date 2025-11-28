# Video Translator Frontend

Next.js frontend for AI video translation with animated UI.

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Aceternity UI (animated backgrounds)
- Framer Motion (animations)
- React Dropzone (file upload)

## Installation

```bash
npm install
# or
yarn install
```

## Running Locally

```bash
npm run dev
# or
yarn dev
```

App will be available at `http://localhost:3000`

## Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set to your Railway backend URL:
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## Deployment to Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL` = your Railway backend URL
4. Deploy

Vercel will auto-detect Next.js and configure build settings.

## Features

- Drag-and-drop video upload
- URL input (YouTube, TikTok, Instagram)
- Real-time processing status with progress bar
- Animated ripple background effect
- Language selection dropdowns
- Video preview and download
- Error handling with alerts
- Responsive design

## UI Components

- **FileUpload**: Drag-and-drop with animation
- **SearchBar**: URL input with animated focus
- **BackgroundRipple**: Animated gradient background
- **Progress**: Processing status bar
- Custom cards, buttons, badges from shadcn/ui

## Project Structure

```
video-translator-frontend/
├── app/
│   ├── globals.css             # Tailwind + custom styles
│   ├── layout.tsx              # Root layout
│   └── page.tsx                # Main page component
├── components/
│   └── ui/
│       ├── file-upload.tsx     # Drag-and-drop component
│       ├── search-bar.tsx      # URL input component
│       ├── background-ripple.tsx
│       ├── button.tsx
│       ├── card.tsx
│       ├── select.tsx
│       ├── progress.tsx
│       └── badge.tsx
├── lib/
│   └── utils.ts                # Utility functions
└── public/                     # Static assets
```

## Customization

### Colors
Edit `globals.css` to change theme colors (currently dark mode with cyan/blue accents).

### Animations
Modify `background-ripple.tsx` and `background-ripple-effect.tsx` for different effects.

### Supported Languages
Add more languages in `page.tsx` Select components (must also update backend).

## Notes

- File size limit: 100MB
- Supported formats: MP4, MOV, AVI, MKV, WEBM
- URL downloads currently not implemented (placeholder)
- Animations use CSS variables for theming
