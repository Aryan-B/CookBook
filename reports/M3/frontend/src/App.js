import './App.css';
import Dragdrop from './components/dragdrop';
import RecipeList from './components/recipelist';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import {AnimatePresence} from 'framer-motion'



function App() {
  return (
    
    <div className="App">
      
      <Router>
        <AnimatePresence>
        <Switch>
        <Route path="/" exact component={Dragdrop}/>
        <Route path="/list"  component={RecipeList}/>
        </Switch>
        </AnimatePresence>
      </Router>
      

    </div>

  );
}

export default App;
