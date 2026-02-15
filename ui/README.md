# PDF to Podcast - Frontend Application

A modern, feature-rich React application for generating podcast-style audio from PDF documents.

## Features

- 📤 **PDF Upload** - Drag-and-drop PDF upload with validation
- 🎙️ **Voice Selection** - Choose from 6 professional AI voices
- ✏️ **Script Editor** - Review and edit generated scripts
- 🎵 **Audio Player** - Play and download podcast audio with waveform visualization
- 📊 **Progress Tracking** - Real-time status updates
- 💾 **Project Management** - View and manage past projects
- ⚙️ **Settings** - Configure preferences and API keys

## Technology Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Redux Toolkit** - State management
- **React Router** - Navigation
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Dropzone** - File uploads
- **WaveSurfer.js** - Audio visualization
- **Framer Motion** - Animations
- **Lucide React** - Icons
- **React Hot Toast** - Notifications

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Progress.jsx
│   │   │   ├── Spinner.jsx
│   │   │   ├── Alert.jsx
│   │   │   └── StepIndicator.jsx
│   │   ├── layout/          # Layout components
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Layout.jsx
│   │   └── features/        # Feature-specific components
│   │       ├── PDFUploader.jsx
│   │       ├── VoiceSelector.jsx
│   │       ├── ScriptEditor.jsx
│   │       ├── AudioPlayer.jsx
│   │       └── ProgressTracker.jsx
│   ├── pages/               # Page components
│   │   ├── Home.jsx
│   │   ├── Generate.jsx
│   │   ├── Projects.jsx
│   │   └── Settings.jsx
│   ├── store/               # Redux store
│   │   ├── store.js
│   │   └── slices/
│   │       ├── projectSlice.js
│   │       ├── uploadSlice.js
│   │       ├── scriptSlice.js
│   │       ├── audioSlice.js
│   │       └── uiSlice.js
│   ├── services/            # API services
│   │   └── api.js
│   ├── hooks/               # Custom hooks
│   │   ├── usePolling.js
│   │   ├── useAudioPlayer.js
│   │   ├── useWaveSurfer.js
│   │   └── useDebounce.js
│   ├── utils/               # Utility functions
│   │   └── helpers.js
│   ├── App.jsx              # Root component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── public/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## Components

### UI Components

**Button** - Versatile button component with variants, sizes, and loading states
```jsx
<Button variant="primary" size="lg" loading={false} icon={Upload}>
  Upload File
</Button>
```

**Card** - Container component with header, body, and footer sections
```jsx
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
  <CardFooter>Actions</CardFooter>
</Card>
```

**Progress** - Progress bar with percentage display
```jsx
<Progress value={75} max={100} showLabel />
```

**Modal** - Customizable modal dialog
```jsx
<Modal isOpen={true} onClose={handleClose} title="Modal Title">
  Content
</Modal>
```

**Alert** - Notification messages with variants
```jsx
<Alert variant="success" title="Success" message="Operation completed" />
```

**StepIndicator** - Multi-step progress indicator
```jsx
<StepIndicator steps={steps} currentStep={2} />
```

### Feature Components

**PDFUploader** - Drag-and-drop PDF upload with validation
- File type validation (PDF only)
- File size validation (max 10MB)
- Upload progress tracking
- Error handling

**VoiceSelector** - Voice selection interface
- 6 AI voice options
- Voice preview/sample playback
- Visual selection state
- Host and guest voice selection

**ScriptEditor** - Interactive script editing
- Add/remove dialogue lines
- Edit speaker assignments
- Edit dialogue text
- Save changes to backend

**AudioPlayer** - Full-featured audio player
- WaveSurfer.js waveform visualization
- Play/pause controls
- Skip forward/backward (10s)
- Time display
- Download functionality

**ProgressTracker** - Real-time progress display
- Animated progress bar
- Step-by-step status
- Progress percentage
- Status messages

## State Management

Redux Toolkit slices:

- **project** - Project list and management
- **upload** - PDF upload state
- **script** - Script generation and editing
- **audio** - Audio generation and playback
- **ui** - UI state (current step, sidebar, theme)

## Custom Hooks

- **usePolling** - Poll async functions at intervals
- **useAudioPlayer** - Audio playback functionality
- **useWaveSurfer** - WaveSurfer.js integration
- **useDebounce** - Debounce values

## API Integration

All API calls are handled through the `services/api.js` module:

```javascript
import { uploadAPI, scriptAPI, audioAPI, voiceAPI } from '@services/api';

// Upload PDF
await uploadAPI.uploadFile(file, (progress) => console.log(progress));

// Generate script
await scriptAPI.generate(jobId, hostVoice, guestVoice);

// Generate audio
await audioAPI.generate(jobId);

// Download audio
await audioAPI.download(jobId);
```

## Pages

### Home (`/`)
- Landing page with features
- Call-to-action buttons
- How it works section

### Generate (`/generate`)
- Main workflow page
- 4-step process:
  1. PDF Upload
  2. Voice Selection
  3. Script Review
  4. Audio Generation
- Real-time progress tracking
- State persistence

### Projects (`/projects`)
- List of all projects
- Project cards with status
- Download/delete actions
- Empty state handling

### Settings (`/settings`)
- API key configuration
- Voice preferences
- App information

## Styling

Tailwind CSS is used for all styling with custom configuration:

- Custom color palette (primary, secondary, success, warning, error)
- Custom animations (fade-in, slide-up, slide-down)
- Responsive design
- Dark mode ready (future feature)

## Error Handling

- Global error boundary
- API error handling with user-friendly messages
- Form validation
- Network error recovery
- Toast notifications for user feedback

## Performance Optimizations

- Code splitting with React.lazy
- Memoized components with React.memo
- Optimized re-renders with useCallback/useMemo
- Virtualized lists for large datasets
- Debounced input handlers
- Lazy loading of images and components

## Testing

```bash
# Run tests
npm run test

# Run tests with coverage
npm run test:coverage
```

## Build & Deployment

```bash
# Build for production
npm run build

# The dist/ folder contains the production build
# Deploy to any static hosting service:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - GitHub Pages
```

## Deployment Checklist

- [ ] Update `VITE_API_URL` for production
- [ ] Enable production error tracking (Sentry, etc.)
- [ ] Configure CDN for static assets
- [ ] Enable gzip/brotli compression
- [ ] Set up SSL certificate
- [ ] Configure CORS on backend
- [ ] Test all features in production environment

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run linting and tests
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
