import { useContext } from 'react';
import { sample } from '../constants/gallary';
import { SendContext } from '../pages/Predict';

const Gallary = () => {
  const { setImage } = useContext(SendContext);

  const fetchImage = async (imageUrl: string): Promise<File> => {
    const response = await fetch(imageUrl);
    const imageBlob = await response.blob();
    return new File([imageBlob], `${imageUrl}.jpg`, {
      type: 'image/jpeg',
    });
  };

  return (
    <div className='bg-white border-b rounded-lg border-gray-200 dark:bg-gray-700 dark:border-blue-500 py-4 sm:py-6 lg:py-8 my-4 sm:my-6 lg:my-8'>
      <div className='mx-auto max-w-screen-2xl px-4 md:px-8'>
        <div className='mb-6 md:mb-10'>
          <h2 className='mb-2 text-center text-2xl font-bold text-cyan-600 dark:text-cyan-200 md:mb-4 lg:text-3xl'>
            Samples
          </h2>
          <span className='text-center text-sm text-gray-700 dark:text-gray-400 lg:text-lg'>
            迷ったらサンプル画像をクリックして分類！
          </span>
        </div>

        <div className='grid grid-cols-2 gap-4 sm:grid-cols-3 md:gap-6 xl:gap-8'>
          {sample.map((sample) => (
            <div
              className='group relative flex h-48 items-end justify-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-96'
              key={sample.id}
              onClick={async () => {
                const file = await fetchImage(sample.image);
                setImage(file);
              }}
            >
              <img
                src={sample.image}
                loading='lazy'
                alt={`sample-${sample.id}`}
                className='absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110'
              />

              <div className='pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50'></div>

              <span className='relative mr-3 mb-3 inline-block rounded-lg border border-gray-500 px-2 py-1 text-xs text-gray-200 backdrop-blur md:px-3 md:text-sm'>
                {sample.id}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Gallary;
