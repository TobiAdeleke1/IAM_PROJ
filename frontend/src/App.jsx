import * as React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import SideMenu from './components/SideMenu';
import MainGrid from './pages/MainGrid';
import ResultDropDown from './pages/ResultDropDown';
import AnalyticsDropDown from './pages/AnalyticsDropDown';
import { QueryProvider }  from './context/QueryContext';
import AppTheme from './theme/AppTheme';

export default function App(props) {

  return (
    <QueryProvider>
      <BrowserRouter>
       <AppTheme>
        <Box sx={{display : 'flex'}}>

          <SideMenu />
          <Box
            component="main"
              sx={(theme) => ({
                flexGrow: 1,
                backgroundColor: theme.vars
                  ? `rgba(${theme.vars.palette.background.defaultChannel} / 1)`
                  : alpha(theme.palette.background.default, 1),
    
                overflow: 'auto',
              })}
          >
          
          <Routes>
            
            <Route path="/" element={<MainGrid />} />
            <Route path="/home" element={<MainGrid />} />
      
            <Route path="/results/:query" element={<ResultDropDown />} />

            <Route path="/analytics" element={<AnalyticsDropDown />} />
          </Routes>
  
        
          </Box>
        </Box>
      </AppTheme>

     </BrowserRouter>
    </QueryProvider>
  
  );
}

