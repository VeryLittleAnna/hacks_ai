import React, { useState, useEffect } from 'react';
import InputButton from './components/UI/button/InputButton'
import YandexMap from './components/ymap/YandexMap'
import styles from './styles/App.module.css';

function App() {
  const [selectedAddress, setSelectedAddress] = useState('');
  const [coordinates, setCoordinates] = useState(null);

  useEffect(() => {
    if (selectedAddress) {
      fetch(`https://geocode-maps.yandex.ru/1.x/?apikey=a1ce5567-b8ef-4cc7-91e1-9d5b2a65adbf&format=json&geocode=${selectedAddress}`)
        .then(response => response.json())
        .then(data => {
          const featureMember = data.response.GeoObjectCollection.featureMember;
          if (featureMember.length > 0) {
            const coords = featureMember[0].GeoObject.Point.pos.split(' ').map(Number);
            console.log([coords[1], coords[0]]);
            setCoordinates([coords[1], coords[0]]);
          } else {
            console.error("Error converting address to coordinates: Empty response data");
          }
        })
        .catch(error => {
          console.error("Error converting address to coordinates:", error);
        });
    }
  }, [selectedAddress, setCoordinates]);

  const handleAddressSubmit = (address) => {
    setSelectedAddress(address);
  };

  return (
    <div className={styles.MyBackground}>
        <InputButton onSubmit={handleAddressSubmit}/>
        <YandexMap coords={coordinates}/>
    </div>
  );
}

export default App;
