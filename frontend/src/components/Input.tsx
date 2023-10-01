import { useRef, useState } from 'react';
import { GiPenguin } from 'react-icons/gi';

interface InputProps {
  profileImage: string;
  setProfileImage: React.Dispatch<React.SetStateAction<string>>;
}

const Input: React.FC<InputProps> = ({ profileImage, setProfileImage }) => {
  const [isTooltip, setIsTooltip] = useState<boolean>(false);
  const inputRef = useRef<HTMLInputElement>(null!);

  const onProfileButtonClick = () => {
    // useRef<HTMLInputElement>のcurrent要素を呼び出し、ファイル選択画面を表示
    inputRef.current.click();
  };

  const onFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    // React.ChangeEvent<HTMLInputElement>よりファイルを取得
    const fileObject = e.target.files[0];
    // オブジェクトURLを生成し、useState()を更新
    setProfileImage(window.URL.createObjectURL(fileObject));
  };

  return (
    <div className='items-center mt-8'>
      <div className='flex items-center justify-center'>
        {profileImage ? (
          <img src={profileImage} className='object-contain h-32 w-32' />
        ) : (
          <></>
        )}
      </div>
      <input
        hidden
        ref={inputRef}
        type='file'
        accept='image/*'
        onChange={onFileInputChange}
      />
      {/* ファイル選択用のボタンを用意 */}
      <button
        className='button outline-violet-900  text-violet-900 hover:bg-violet-900 hover:text-white'
        onClick={onProfileButtonClick}
        onMouseMove={() => setIsTooltip(true)}
        onMouseLeave={() => setIsTooltip(false)}
      >
        分類する画像を選択
      </button>
      {isTooltip && (
        <div className='absolute mt-4 text-gray-400 rounded text-xs flex items-center'>
          <GiPenguin />
          HINT: お気に入りのペンギンを選択してね
          <GiPenguin className='transform scale-x-[-1]' />
        </div>
      )}
    </div>
  );
};

export default Input;
