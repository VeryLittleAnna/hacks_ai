import React, { useState, useEffect } from 'react';
import { YMaps, Map, Placemark, ZoomControl } from 'react-yandex-maps';
import styles from './YandexMap.module.css';

function YandexMap(props) {
  const [mapState, setMapState] = useState({
    center: props.coords || [59.941363540794505, 30.316168935546784],
    zoom: 12,
  });

  useEffect(() => {
    if (props.coords) {
      setMapState(prevState => ({
        ...prevState,
        center: props.coords,
      }));
    }
  }, [props.coords]);

  const handlePlacemarkClick = (coordinates) => {
    setMapState(prevState => ({
      ...prevState,
      center: coordinates,
    }));
  };

  return (
    <div className={styles.MyDiv}>
      <YMaps>
        <div style={{ borderRadius: '20px', overflow: 'hidden' }}>
          <Map defaultState={mapState} 
          width="815px" 
          height="535px">
              <Placemark
                geometry={props.coords}
                onClick={() => handlePlacemarkClick(props.coords)}
              />
            <ZoomControl options={{float: 'right'}}/>
          </Map>
        </div>
      </YMaps>
    </div>
  );
}

export default YandexMap;
