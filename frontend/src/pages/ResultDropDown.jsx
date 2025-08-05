import * as React from 'react';
import { useParams } from 'react-router';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useAuth0 } from '@auth0/auth0-react';
import { useQuery } from '../context/QueryContext';
import DataTable from '../components/DataTable';

import { 
  fetchPostCodeData,
  extractRelevantPostcodeField,
  fetchAllData
} from '../utils/helper';


export default function ResultDropdown(){
  const { query } = useParams();
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();
  const { setQuery } = useQuery();

  const [loading, setLoading ] = React.useState(null);
  const [data, setData] = React.useState({});
  const [errors, setErrors] = React.useState({});

  React.useEffect(()=>{
      setQuery(query);
  }, [query, setQuery]);

  React.useEffect(() => {
    const fetchResult = async () =>{

      setLoading(true);
      setErrors({});
      setData({});

      try{
        
        const postcode = await fetchPostCodeData(query, setErrors);
        if (!postcode) return;

        const updatedpostcode = await extractRelevantPostcodeField(postcode);
        const postcodeName = updatedpostcode.postcode;
        const localAuthorityName = updatedpostcode.admin_district;
 
        if (!isAuthenticated){
            setData({ updatedpostcode: [updatedpostcode]});
              
        }else{

          const otherData = await fetchAllData(
            postcodeName,
            localAuthorityName,
            getAccessTokenSilently, 
            setErrors
          );

          const newData = {
            updatedpostcode: [updatedpostcode],
            ...otherData
          }

          setData(newData);
        }
        
      
      }catch(err){
        setErrors(prev => ({...prev, general: `Unexpected error ${err}`}));

      }finally{
        
        setLoading(false);
      }
         
    };
    fetchResult();
    }, [query, getAccessTokenSilently, isAuthenticated]);

    const sections = [
      {key: 'updatedpostcode', label: 'Postcode Lookup'},
      {key: 'pricepaid', label: 'Price Paid'},
      {key: 'planningapplication', label: 'Planning Application'},
      {key: 'financeborrowing', label: 'Finance Borrowing'},
      {key: 'financeinvestment', label: 'Finance Investment'},
      {key: 'quarterlyrevenue', label: 'Quarterly Revenue'}
    ];

    return (
        <Box 
        sx={{ p: 4 }}>
        
       
         <Typography variant="h4">Results for: {query}</Typography>

         {loading && <CircularProgress sx={{mt: 2}}/>}
      
        {!loading && (
          <>
            {sections.map(({ key, label }) => (
              <Accordion key={key} defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6">{label}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  {errors[key] && (
                    <Typography color="error" sx={{ mb: 2 }}>
                      {errors[key]}
                    </Typography>
                  )}
                  {data[key] ? <DataTable data={data[key]} /> 
                  : !errors[key] && (
                    <Typography variant="body2">No data available.</Typography>
                  )}
                </AccordionDetails>
              </Accordion>
            ))}
          </>
        )}
      </Box>
    
    );
}