import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ErrorBoundary } from './components/ErrorBoundary.tsx'
import { AuthProvider } from './contexts/AuthContext.tsx'
import './index.css'
import App from './App.tsx'

console.log('main.tsx: Application starting...')

console.log('main.tsx: Creating root...')
const rootElement = document.getElementById('root')

if (!rootElement) {
  console.error('main.tsx: Failed to find root element')
} else {
  try {
    const root = createRoot(rootElement)
    console.log('main.tsx: Rendering application...')
    root.render(
      <StrictMode>
        <ErrorBoundary>
          <AuthProvider>
            <App />
          </AuthProvider>
        </ErrorBoundary>
      </StrictMode>
    )
    console.log('main.tsx: Application rendered successfully')
  } catch (error) {
    console.error('main.tsx: Error rendering application:', error)
  }
}
