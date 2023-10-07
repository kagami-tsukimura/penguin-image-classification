const NotFound = () => {
  return (
    <div className='bg-white py-6 sm:py-8 lg:py-12'>
      <div className='mx-auto max-w-screen-2xl px-4 md:px-8'>
        <div className='relative mx-auto flex h-96 w-full items-center justify-center overflow-hidden rounded-lg bg-gray-100 shadow-lg sm:w-96'>
          <img
            src='https://images.unsplash.com/photo-1530651788726-1dbf58eeef1f?auto=format&q=75&fit=crop&w=600'
            loading='lazy'
            alt='Photo by Connor Botts'
            className='absolute inset-0 h-full w-full object-cover object-center'
          />

          <div className='relative flex flex-col items-center justify-center p-8 md:p-16'>
            <h1 className='mb-2 text-center text-2xl font-bold text-white md:text-3xl lg:text-4xl'>
              404
            </h1>

            <p className='mb-8 text-center text-gray-200 md:text-lg'>
              The page you’re looking for doesn’t exist.
            </p>

            <a
              href='#'
              className='inline-block rounded-lg bg-gray-200 px-8 py-3 text-center text-sm font-semibold text-gray-500 outline-none ring-indigo-300 transition duration-100 hover:bg-gray-300 focus-visible:ring active:text-gray-700 md:text-base'
            >
              Go home
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
