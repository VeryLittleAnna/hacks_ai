import React, { useState, useRef, useEffect } from 'react';
import styles from './InputButton.module.css';
import axios from 'axios';
import Icon from '@mdi/react';
import { mdiArrowRightCircleOutline, mdiAlertBoxOutline, mdiCloseCircleOutline, mdiCheckCircleOutline } from '@mdi/js';
import logo from './logo.png';

function InputButton(props) {
  const [address, setAddress] = useState('');
  const [file, setFile] = useState(null);
  const [ref_file, setRef_File] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [showAnswersReadyMessage, setShowAnswersReadyMessage] = useState(false);
  const [showUploadMessage, setShowUploadMessage] = useState(false);
  const [fileType, setFileType] = useState(null);

  const ref = useRef();

  useEffect(() => {
    // Исчезновение всплывающего сообщения через 10 секунд
    if (showAnswersReadyMessage) {
      const timeoutId = setTimeout(() => {
        setShowAnswersReadyMessage(false);
      }, 10000);

      return () => clearTimeout(timeoutId);
    }
  }, [showAnswersReadyMessage]);

  useEffect(() => {
    // Исчезновение всплывающего сообщения через 10 секунд
    if (showUploadMessage) {
      const timeoutId = setTimeout(() => {
        setShowUploadMessage(false);
      }, 10000);

      return () => clearTimeout(timeoutId);
    }
  }, [showUploadMessage]);

  useEffect(() => {
    if (errorMessage !== null) {
      // Исчезновение всплывающего сообщения об ошибке через 10 секунд
      const timer = setTimeout(() => {
        setErrorMessage(null);
      }, 10000);

      return () => clearTimeout(timer);
    }
  }, [errorMessage]);

  const reset = () => {
    ref.current.value = null;
    setAddress('');
  };

  const handleChange = (event) => {
    setAddress(event.target.value);
  };

  const handleFileChange = (event, fileType) => {
    setFileType(fileType);
    if (fileType === 'file') {
      setFile(event.target.files[0]);
    } else if (fileType === 'file_ref') {
      setRef_File(event.target.files[0]);
    }
    setShowUploadMessage(true);
  };

  const handleGetCoordinates = async () => {
    try {
      const formData = new FormData();

      if (fileType === 'file') {
        formData.append('file', file);
        setFile(null);
      } else if (fileType === 'file_ref') {
        formData.append('file_ref', ref_file);
        setRef_File(null);
      } else {
        formData.append('address', address);
        setAddress('');
      }
      const response = await axios.post('http://localhost:8000/api/get_coordinates/', formData);
      console.log(response.data.success, response.data.target_address, response.data.message_file);
      if (response.data.success) {
        if (response.data.message_file) {
          console.log("Ответы записаны в лог!");
          setShowAnswersReadyMessage(true); // Показываем сообщение о готовности ответов
        } else {
          props.onSubmit(response.data.target_address);
        }
      } else {
        console.log('Failed to get coordinates');
        setErrorMessage('No coordinates found for the address.');
      }
    } catch (error) {
      console.error('Error fetching coordinates:', error);
      setErrorMessage('An error occurred while fetching coordinates. Please try again.');
    }
  };
  

  return (
    <div>
      <img src={logo} className={styles.MyLogo} />
      <div className={styles.MyDiv}>
        <input
          type="text"
          value={address}
          onChange={handleChange}
          className={styles.MyInput}
          placeholder="Введите адрес"
        />

        <div className={styles.dowloadInp}>
          <input
            id="fileInput"
            type="file"
            onChange={(event) => handleFileChange(event, 'file')}
            ref={ref}
            accept=".csv"
            style={{ display: 'none' }}
          />

          <label
            htmlFor="fileInput"
            className={styles.uploadLabel}> Загрузить данные</label>
        </div>

        <div className={styles.dowloadRef}>
          <input
            id="fileRefInput"
            type="file"
            onChange={(event) => handleFileChange(event, 'file_ref')}
            ref={ref}
            accept=".csv"
            style={{ display: 'none' }}
          />

          <label
            htmlFor="fileRefInput"
            className={styles.uploadRefLabel}> Загрузить эталоны</label>
        </div>

        <button onClick={handleGetCoordinates} className={styles.MyBtn}>
          Отправить <Icon path={mdiArrowRightCircleOutline} size={0.8} />
        </button>

        <button onClick={reset} className={styles.ClearBtn}>
          Очистить <Icon path={mdiCloseCircleOutline} size={0.8} />
        </button>
      </div>

      {showAnswersReadyMessage && (
        <div className={styles.uploadMessage}>
          <Icon path={mdiCheckCircleOutline} size={1} /> {"Ответы готовы!"}
        </div>
      )}

      {showUploadMessage && (
        <div className={styles.uploadMessage}>
          <Icon path={mdiCheckCircleOutline} size={1} /> {"Файл загружен и готов к отправке!"}
        </div>
      )}

      {errorMessage !== null && (
        <div className={styles.MyErrorMessage}>
          <Icon path={mdiAlertBoxOutline} size={1} /> {errorMessage}
        </div>
      )}

    </div>
  );
}

export default InputButton;
