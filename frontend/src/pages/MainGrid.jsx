import * as React from 'react';
import Box from '@mui/material/Box';
import Search from '../components/Search';

export default function MainGrid(){
    return (
        <Box 
        sx={{ 
          width: '100%',
          maxWidth: { sm: '100%', md: '1700px' },
          height: '100vh',
          display: 'flex',
          alignItems: 'center' ,
          justifyContent: 'center'
          }}>
       
          <Search />
        
        </Box>
    )
}