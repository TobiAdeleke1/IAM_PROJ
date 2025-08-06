import * as React from 'react';
import { useNavigate } from 'react-router';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { PieChart } from '@mui/x-charts/PieChart';
import { useAuth0 } from '@auth0/auth0-react';
import { useQuery } from '../context/QueryContext';
import { Card } from '@mui/material';
import { BarChart } from '@mui/x-charts/BarChart';

import { 
  fetchPostCodeData,
  extractRelevantPostcodeField,
  fetchAllData,
  pricePaidAnalytics,
  planningapplicationAnalytics,
  quarterlyrevenueAnalytics
} from '../utils/helper';


export default function AnalyticsDropDown(){
    const { query } = useQuery();
    const { isAuthenticated, getAccessTokenSilently } = useAuth0();
    const navigate = useNavigate();

    const [loading, setLoading ] = React.useState(null);
    const [data, setData] = React.useState({});
    const [dataAnalytics, setDataAnalytics] = React.useState({});
    const [errors, setErrors] = React.useState({});
 
    React.useEffect(() =>{
      const fetchAnalytics = async () =>{
          setLoading(true);
          setErrors({});
          setData({});
          setDataAnalytics({});

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

                const { pricepaid, planningapplication, quarterlyrevenue  } = newData;
                const postcodeDataAnalytics = await pricePaidAnalytics(pricepaid);
                const planningapplicationDataAnalytics = await planningapplicationAnalytics(planningapplication);
                const quarterlyrevenueDataAnalytics = await quarterlyrevenueAnalytics(quarterlyrevenue);
               

                
                setDataAnalytics({
                  pricepaid: postcodeDataAnalytics,
                  planningapplication: planningapplicationDataAnalytics,
                  financeborrowing: {},
                  quarterlyrevenue: quarterlyrevenueDataAnalytics

                })
               

              }
              
            
            }catch(err){
              setErrors(prev => ({...prev, general: `Unexpected error ${err}`}));
      
            }finally{
              
              setLoading(false);
            }
                   


        };
      fetchAnalytics();

    }, [query, getAccessTokenSilently]);

  const sections = [
    {
      key: 'pricepaid',
      label: 'Price Paid',
      display: (
        <Card sx={{ p: 3, mb: 2 }}>
          <Typography variant="h5">Total Records</Typography>
          <Typography variant="h2">
            {dataAnalytics.pricepaid ? dataAnalytics.pricepaid.pricePaidCount : 0}
          </Typography>
          <Typography variant="h5">Average Records</Typography>
          <Typography variant="h2">
            {dataAnalytics.pricepaid ? dataAnalytics.pricepaid.average : 0}
          </Typography>
        </Card>
      ),
    },
    {
      key: 'planningapplication',
      label: 'Planning Application',
      display: (
        <BarChart
          xAxis={[{ scaleType: 'band', data: dataAnalytics?.planningapplication?.years ?? []  }]}
          series={[
            {
              data: dataAnalytics?.planningapplication?.total ?? [],
              label: 'Total Decisions',
            },
            {
              data: dataAnalytics?.planningapplication?.granted ?? [],
              label: 'Total Granted',
            },
            {
              data: dataAnalytics?.planningapplication?.refused ?? [],
              label: 'Total Refused',
            }
          ]}
          width={600}
          height={400}
        />
      ),
    },
    {
      key: 'quarterlyrevenue',
      label: 'Quarterly Revenue',
      display: (
        <PieChart
          series={[
            {
              data: dataAnalytics?.quarterlyrevenue ?? []
            },
          ]}
          width={300}
          height={200}
        />
      ),
    },
    {
      key: 'financeborrowing',
      label: 'Finance Borrowing',
      display: <Card sx={{ p: 2 }}>[Borrowing Placeholder]</Card>,
    },
    {
      key: 'financeinvestment',
      label: 'Finance Investment',
      display: <Card sx={{ p: 2 }}>[Investment Placeholder]</Card>,
    },
  ];

    
    React.useEffect(() =>{
        if(query === null){
            navigate("/home");   
    }
    }, [query, navigate])
    

    return (
        <Box 
        sx={{ p: 4 }}>
        
       
         <Typography variant="h4">Results for Analytics : {query}</Typography>

         {loading && <CircularProgress sx={{mt: 2}}/>}
      
        {!loading && (
          <>
            {sections.map(({ key, label, display }) => (
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
                  {data[key] ? display
                  : !errors[key] && (
                    <Typography variant="body2">No data available.</Typography>
                  )}
                </AccordionDetails>
              </Accordion>
            ))}
          </>
        )}
      </Box>
    
    )
}