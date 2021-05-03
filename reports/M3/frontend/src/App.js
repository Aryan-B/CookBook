import './App.css';
import Dragdrop from './components/dragdrop';
import RecipeList from './components/recipelist';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';




function App() {
  return (
    
    <div className="App">
      <h1>CookBook</h1>
      <Router>
        <Switch>
        <Route path="/" exact component={Dragdrop}/>
        <Route path="/list"  component={RecipeList}/>
        </Switch>
      </Router>
      

    </div>

  );
}

export default App;
