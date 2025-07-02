import { useAuth0 } from "@auth0/auth0-react";

import * as React from 'react';
import { styled } from '@mui/material/styles';
import Divider from '@mui/material/Divider';
import MuiDrawer, { drawerClasses } from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import MenuContent from './MenuContent';
import LogoutButton from './LogOutButton';
import LogInButton from './LogInButton';


const drawerWidth = 240;

const Drawer = styled(MuiDrawer)({
    width: drawerWidth,
    flexShrink: 0,
    boxSizing: 'border-box',
    mt: 10,
    [`& .${drawerClasses.paper}`]:{
        width: drawerWidth,
        boxSizing: 'border-box'
    }

});

export default function SideMenu(){
    const { isAuthenticated }  = useAuth0();
    return (
        <Drawer
            variant='permanent'
            sx={{
                display: {xs: 'none', md: 'block'},
                [`& .${drawerClasses.paper}`]: {
                    backgroundColor: 'background.paper',      
                },
            }}
        
        >

        <Box
            sx={{
            display: 'flex',
            mt: 'calc(var(--template-frame-height, 0px) + 4px)',
            p: 1.5,
            }}
        >
         Replace the Select
        </Box>
        <Divider/>
        <Box
            sx={{
            overflow: 'auto',
            height: '100%',
            display: 'flex',
            flexDirection: 'column'
            }}
        >
        <MenuContent />
  

        </Box>
        <Stack
            direction="row"
            sx={{
                p: 2,
                gap: 1,
                alignItems: 'center',
                borderTop: '1px solid',
                 borderColor: 'divider',

            }}
        
        >

        {!isAuthenticated && (
            <>
                <LogInButton />
            </>)}
        
         {isAuthenticated && (
            <>
                <LogoutButton />
            </>)}

        </Stack>

        </Drawer>
    )
}