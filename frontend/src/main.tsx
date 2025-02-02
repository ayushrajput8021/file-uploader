import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import { Toaster } from 'sonner';

import './index.css';
import { ThemeProvider } from './components/theme-provider.tsx';

ReactDOM.createRoot(document.getElementById('root')!).render(
	<React.StrictMode>
		<ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
			<Toaster />
			<App />
		</ThemeProvider>
	</React.StrictMode>
);
