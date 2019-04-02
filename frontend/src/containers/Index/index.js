import Index from './Index'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux'
import { storeGeoLocationData } from '../../actions/geoLocationAction'


const mapStatToProps = (state) => {
    return {
        geo: state.geoLocationReducer.geoLocationData
    }
};

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators({
        storeGeoLocationData
    }, dispatch);
};

export default connect(mapStatToProps, mapDispatchToProps)(Index)