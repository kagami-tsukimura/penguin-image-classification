import './App.css';
import Footer from './components/Footer';
import Header from './components/Header';
import Input from './components/Input';
import Output from './components/Output';

const App: React.FC = () => {
  return (
    <>
      <Header />
      <div className='flex items-center justify-between'>
        <Input />
        <Output />
      </div>
      <Footer />
    </>
  );
};

export default App;
