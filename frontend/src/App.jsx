import * as React from 'react';
import { BrowserRouter, Routes, Route } from "react-router"
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import SideMenu from './components/SideMenu';
import Stack from '@mui/material/Stack';
import MainGrid from './components/MainGrid';
import AppTheme from './theme/AppTheme';

export default function App(props) {

  return (
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
          <Route path="/home" element={<MainGrid />} />
           <Route path="/" element={<MainGrid />} />
         </Routes>
 
      
        </Box>
      </Box>
    </AppTheme>

     </BrowserRouter>
   
 

  )
}

