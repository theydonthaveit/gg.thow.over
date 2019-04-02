const initialState = {
    geoLocationData: null
}

export const geoLocationReducer = (state = initialState, action) => {
    switch (action.type) {
        case "STORE_GEOLOCATION_DATA":
            let { value } = action.payload.target
            return {
                ...state,
                geoLocationData: value
            }
        default:
            return state
    }
}