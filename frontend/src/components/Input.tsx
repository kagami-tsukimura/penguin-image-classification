import { useState } from 'react';

const Input = () => {
  const [imageMessage, setImageMessage] =
    useState('分類したい画像を選択してください');
  const [profileImage, setProfileImage] = useState('default-profile.png');
  const onFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    // React.ChangeEvent<HTMLInputElement>よりファイルを取得
    const fileObject = e.target.files[0];
    // オブジェクトURLを生成し、useState()を更新
    setImageMessage('');
    setProfileImage(window.URL.createObjectURL(fileObject));
  };

  return (
    <div className='items-center mt-8'>
      <p className='text-left mb-8'>{imageMessage}</p>
      <div className='flex items-center justify-center'>
        <img src={profileImage} className='h-32 w-32 rounded-full' />
      </div>
      <input
        type='file'
        accept='image/*'
        onChange={onFileInputChange}
        className='items-center pt-8'
      />
    </div>
  );
};

export default Input;
