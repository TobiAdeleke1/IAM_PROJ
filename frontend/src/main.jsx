import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Auth0Provider } from '@auth0/auth0-react'
import App from './App.jsx'

const DOMAIN = import.meta.env.VITE_AUTH_DOMAIN || "";
const CLIENT_ID = import.meta.env.VITE_AUTH_CLIENT_ID || "";
const AUTH_AUDIENCE = import.meta.env.VITE_AUTH_AUDIENCE || "";
const REDIRECT_URI = `${window.location.origin}/home`;


createRoot(document.getElementById('root')).render(
  <StrictMode>
  <Auth0Provider
   domain={DOMAIN}
   clientId={CLIENT_ID}
   authorizationParams={{
     redirect_uri: REDIRECT_URI,
     audience: AUTH_AUDIENCE,
   }}
  >
      <App />
  </Auth0Provider>
    
  </StrictMode>,
)
