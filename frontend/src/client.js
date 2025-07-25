const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";


export const getPostcodeLookup = async ( postcode ) =>{
    // const queryParams = new URLSearchParams();
    // queryParams.append("postcode", postcode || "sw1w 9su" );
    const response = await fetch(`https://api.postcodes.io/postcodes/${postcode}`)
    
    if(!response.ok){
        throw new Error("Postcode not found");
    }
    return response.json();

}

export const getPricePaidData = async ( getAccessTokenSilently ) => {

    const token = await getAccessTokenSilently();
 
    const response = await fetch(`${API_BASE_URL}/tier_api/pricepaid`,{
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

export const getPlanningApplicationData = async( getAccessTokenSilently ) =>{
    const token = await getAccessTokenSilently();
    const response = await fetch(`${API_BASE_URL}/tier_api/planningapplication`, {
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

export const getFinanceBorrowingData = async ( getAccessTokenSilently ) =>{
    const token = await getAccessTokenSilently();
    const response = await fetch(`${API_BASE_URL}/tier_api/financeborrowing`,{
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

export const getFinanceInvestmentData = async ( getAccessTokenSilently ) =>{
    const token = await getAccessTokenSilently();
    const response = await fetch(`${API_BASE_URL}/tier_api/financeinvestment`,{
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

export const getQuarterlyRevenueData = async ( getAccessTokenSilently ) =>{
    const token = await getAccessTokenSilently();
    const response = await fetch(`${API_BASE_URL}/tier_api/quarterlyrevenue`,{
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
