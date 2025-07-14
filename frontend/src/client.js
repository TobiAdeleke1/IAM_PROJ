const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export const getPostcodeLookup = async (postcode) =>{
    // const queryParams = new URLSearchParams();
    // queryParams.append("postcode", postcode || "sw1w 9su" );
    const response = await fetch(`https://api.postcodes.io/postcodes/${postcode}`)
    
    if(!response.ok){
        throw new Error("Postcode not found");
    }
    return response.json();

}
