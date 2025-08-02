import * as React from 'react';
import {useNavigate} from 'react-router';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import FormControl from '@mui/material/FormControl';
import InputAdornment from '@mui/material/InputAdornment';
import OutlinedInput from '@mui/material/OutlinedInput';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';

export default function Search() {
  const [query , setQuery] = React.useState("");
  const navigate = useNavigate();

  const handleChange = (event) =>{
    setQuery(event.target.value);

  };

  const handleSubmit = (event) =>{
    event.preventDefault();
    console.log(query);
    if (query.trim() === "") return ;
  
    // Navigate to the result page 
    navigate(`/results/${encodeURIComponent(query.trim())}`)

  };
 
  return (
     
        <Stack
          spacing={2}
          useFlexGap
          sx={{ alignItems: 'center', width: { xs: '100%', sm: '70%' } }}
          
        >
          <Typography
            variant="h2"
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', sm: 'row' },
              alignItems: 'center',
              fontSize: 'clamp(3rem, 10vw, 3.5rem)',
            }}
          >
            Postcode&nbsp;Search&nbsp;
    
          </Typography>
        <form onSubmit={handleSubmit}>
             <FormControl
           fullWidth
           sx={{ width: { xs: '100%', sm: '500px', md: '600px' } }}
           variant="outlined"
           >
            <OutlinedInput
                size="medium"
                id="search"
                placeholder="Search…"
                value={query}
                onChange={handleChange}
                sx={{ flexGrow: 1 }}
                startAdornment={
                  <InputAdornment position="start" sx={{ color: 'text.primary' }}>
                    <SearchRoundedIcon fontSize="small" />
                  </InputAdornment>
                }
                inputProps={{
                  'aria-label': 'search',
                }}
              />
        </FormControl>

        </form>
         
 
        </Stack>
  );
}