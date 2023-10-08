const Gallary = () => {
  return (
    <div className='bg-white border-b border-gray-200 dark:bg-gray-700 dark:border-blue-500 py-6 sm:py-8 lg:py-12'>
      <div className='mx-auto max-w-screen-2xl px-4 md:px-8'>
        <div className='mb-10 md:mb-16'>
          <h2 className='mb-4 text-center text-2xl font-bold text-cyan-600 dark:text-cyan-200 md:mb-6 lg:text-3xl'>
            Samples
          </h2>
        </div>

        <div className='grid grid-cols-2 gap-4 sm:grid-cols-3 md:gap-6 xl:gap-8'>
          <a
            href='#'
            className='group relative flex h-48 items-end justify-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-96'
          >
            <img
              src='https://source.unsplash.com/icFkx8Dy54M'
              loading='lazy'
              alt='Photo by Minh Pham'
              className='absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110'
            />

            <div className='pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50'></div>

            <span className='relative mr-3 mb-3 inline-block rounded-lg border border-gray-500 px-2 py-1 text-xs text-gray-200 backdrop-blur md:px-3 md:text-sm'>
              1
            </span>
          </a>

          <a
            href='#'
            className='group relative flex h-48 items-end justify-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-96'
          >
            <img
              src='https://source.unsplash.com/22EqbN0yI-4'
              loading='lazy'
              alt='Photo by Lorenzo Herrera'
              className='absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110'
            />

            <div className='pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50'></div>

            <span className='relative mr-3 mb-3 inline-block rounded-lg border border-gray-500 px-2 py-1 text-xs text-gray-200 backdrop-blur md:px-3 md:text-sm'>
              2
            </span>
          </a>

          <a
            href='#'
            className='group relative flex h-48 items-end justify-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-96'
          >
            <img
              src='https://source.unsplash.com/DE6yhZyG8bE'
              loading='lazy'
              alt='Photo by Magicle'
              className='absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110'
            />

            <div className='pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50'></div>

            <span className='relative mr-3 mb-3 inline-block rounded-lg border border-gray-500 px-2 py-1 text-xs text-gray-200 backdrop-blur md:px-3 md:text-sm'>
              3
            </span>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Gallary;
