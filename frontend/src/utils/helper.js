import {
  getPostcodeLookup,
  getPricePaidData,
  getPlanningApplicationData,
  getFinanceBorrowingData,
  getFinanceInvestmentData,
  getQuarterlyRevenueData
} from '../client';

export const fetchPostCodeData = async (query, setErrors) =>{
    
    try{
        const response = await getPostcodeLookup(query);
        return response.result;
    }catch(err){
        setErrors(prev => ({ ...prev, updatedpostcode: err.message }));
        return null;

    }
};

export const extractRelevantPostcodeField = async (postcodeResponse) =>{
    const {
        codes, parliamentary_constituency_2024,
        european_electoral_region, eastings,
        northings, longitude, latitude, 
        incode, outcode, nhs_ha,parliamentary_constituency, 
        primary_care_trust, ced, pfa, nuts,
        ccg, lsoa,msoa, ...updatedpostcode 
    } = postcodeResponse;
    return updatedpostcode;
};

export const fetchAllData = async(postcodeName, localAuthorityName, getAccessTokenSilently, setErrors) =>{
    const [
            pricepaid,
            originalPlanningapplication,
            originalFinanceborrowing,
            originalFinanceinvestment,
            originalQuarterlyrevenue,
          ] = await Promise.all([
            getPricePaidData(postcodeName, getAccessTokenSilently).catch(err =>{
              setErrors(prev =>({...prev, pricepaid: err.message}));
              return null;
            }),
            getPlanningApplicationData(localAuthorityName, getAccessTokenSilently).catch(err =>{
              setErrors(prev => ({...prev, planningapplication: err.message}));
              return null;
            }),
            getFinanceBorrowingData(localAuthorityName, getAccessTokenSilently).catch(err =>{
              setErrors(prev => ({...prev, financeborrowing: err.message}));
              return null;
            }),
            getFinanceInvestmentData(localAuthorityName, getAccessTokenSilently).catch(err =>{
              setErrors(prev =>({...prev, financeinvestment: err.message}));
              return null;
            }),
            getQuarterlyRevenueData(localAuthorityName, getAccessTokenSilently).catch(err=>{
              setErrors(prev =>({...prev, quarterlyrevenue: err.message}));
              return null;
            })

          ]);
        
        const planningapplication = originalPlanningapplication.map(( {id, created_at, updated_at, ...rest}) => rest);
        const quarterlyrevenue = originalQuarterlyrevenue.map(( 
          {id, created_at, updated_at, region, class_of_authority, 
           ons_code, e_code, net_current_expenditure_including_education_non_pay_element,
           total_service_expenditure_including_education_non_pay_element,
          housing_revenue_account_income_total, housing_revenue_account_expenditure_total, ...rest}) => rest);
        const financeinvestment = originalFinanceinvestment.map(( {id, created_at,sheet_name, updated_at, ...rest}) => rest);
        const financeborrowing = originalFinanceborrowing.map(( {id, created_at,sheet_name, updated_at, ...rest}) => rest);


    return {
        pricepaid,
        planningapplication,
        financeborrowing,
        financeinvestment,
        quarterlyrevenue
    };
};

export const pricePaidAnalytics = async (postcodeData) =>{
  const postcodeCount = postcodeData.length;
  const postcodeAvg = postcodeData
                       .map(({price}) => parseInt(price))
                       .reduce((currSum, currValue) => currSum+= currValue, 0)/postcodeCount;  
  const maxDate = postcodeData
                  .map(({date_of_transfer}) =>  Date.parse(date_of_transfer))
                  .reduce((maxD, currDate) => Math.max(maxD, currDate), 0);
  const minDate = postcodeData
                  .map(({date_of_transfer}) =>  Date.parse(date_of_transfer))
                  .reduce((minD, currDate) => Math.min(minD, currDate), 0);



  return {
    pricePaidCount: postcodeCount,
    average: postcodeAvg,
    maxDate: Date.parse(maxDate).toLocaleString(),
    minDate: Date.parse(minDate).toLocaleString(),
  
  }
  


}