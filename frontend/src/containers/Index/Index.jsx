import React from 'react';
import styles from './Index.module.css';


const App = ({ geo, storeGeoLocationData }) => {
    if ("geolocation" in navigator) {
        // NOT GEO DATA
        // TODO: change to !geo
        if (geo) {
            navigator.geolocation.getCurrentPosition((position) => {
                fetch(
                    `http://api.postcodes.io/postcodes?lon=
                ${position.coords.longitude}&lat=
                ${position.coords.latitude}`
                ).then((data) =>
                    data.json()
                ).then((json) => {
                    // set GEO DATA
                    // check new GEO DATA if we suspect a change
                    console.log(json.result[0].outcode
                    )
                })
            }, (error) => {
                // provide form to add postcode data
                // present education as to why we need geolocation
                // and how it makes your life easier
                console.log(error)
            })
        }
    } else {
        // enter your own details
    }

    return (
        <div className={styles.app}>
            <form
            // onSubmit={sendGeoLocationData}>
            >
                <input onChange={(e) => storeGeoLocationData(e)} />
                <input type="submit" value="send" />
            </form>
        </div>
    )
}

export default App;