const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";


export const getPostcodeLookup = async ( postcode ) =>{
    const response = await fetch(`https://api.postcodes.io/postcodes/${postcode}`)
    
    if(!response.ok){
        throw new Error("Postcode not found");
    }
    return response.json();

}

export const getPricePaidData = async (query, getAccessTokenSilently ) => {

    const token = await getAccessTokenSilently();
    const queryParams = new URLSearchParams();
    queryParams.append("postcode", query);
 
    const response = await fetch(`${API_BASE_URL}/tier_api/pricepaid/search/?${queryParams.toString()}`,{
        method: 'GET',
        headers:{
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok){
        throw new Error(`${response.message} with error ${response.status}`);
    }

    return response.json();
};


export const getPlanningApplicationData = async( query, getAccessTokenSilently ) =>{

    const token = await getAccessTokenSilently();
    const queryParams = new URLSearchParams();
    queryParams.append("authority_name", query);
    const response = await fetch(`${API_BASE_URL}/tier_api/planningapplication/search/?${queryParams.toString()}`, {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if(!response.ok){
        console.log("planningapplication:", response.message);
        throw new Error(`${response.message} with error ${response.status}`);
    }
    return response.json();
};

export const getFinanceBorrowingData = async (query, getAccessTokenSilently ) =>{
    const token = await getAccessTokenSilently();
    const queryParams = new URLSearchParams();
    queryParams.append("local_authority_name", query);
    const response = await fetch(`${API_BASE_URL}/tier_api/financeborrowing/search/?${queryParams.toString()}`,{
        method: 'GET',
        headers: {
            Authorization: `Bearer ${token}`,
           'Content-Type': 'application/json',
        },
    });

    if(!response.ok){
        throw new Error(`${response.message} with error ${response.status}`);
    };

    return response.json();
};

export const getFinanceInvestmentData = async (query, getAccessTokenSilently ) =>{
    const token = await getAccessTokenSilently();
    const queryParams = new URLSearchParams();
    queryParams.append("local_authority_name", query);
    const response = await fetch(`${API_BASE_URL}/tier_api/financeinvestment/search/?${queryParams.toString()}`,{
        method: 'GET',
        headers: {
            Authorization: `Bearer ${token}`,
           'Content-Type': 'application/json',
        },
    });

    if(!response.ok){
        throw new Error(`${response.message} with error ${response.status}`);
    };

    return response.json();
};

export const getQuarterlyRevenueData = async (query,  getAccessTokenSilently ) =>{
    const token = await getAccessTokenSilently();
    const queryParams = new URLSearchParams();
    queryParams.append("local_authority_name", query);
    const response = await fetch(`${API_BASE_URL}/tier_api/quarterlyrevenue/search/?${queryParams.toString()}`,{
        method: 'GET',
        headers: {
            Authorization: `Bearer ${token}`,
           'Content-Type': 'application/json',
        },
    });

    if(!response.ok){
        throw new Error(`${response.message} with error ${response.status}`);
    };

    return response.json();
};
