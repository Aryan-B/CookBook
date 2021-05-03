import {useEffect, useState} from 'react';
import axios from 'axios';
import './list.css';
function RecipeList(props) {
    const [loaded,setloaded]=useState(false);

    const vals=props.location.state;
    async function fetchMyAPI() {
        let fd= new FormData();
        for (let i = 0 ; i < vals.length ; i++) {
            if(vals[i].type!=='string'){
                console.log(vals[i]);
            fd.append('file'+[i], vals[i]);}
        }
        const response= await axios.post('http://localhost:8080/recognise', fd);
        if(response.data.result==='Success'){
                console.log('success');
                setloaded(true);
            }
            else{
                console.log('aw snap, failed!');
        };    
    }

    useEffect(()=>{
        fetchMyAPI();
    },[]);


    return (      
      <div className="App">
        <h1>Recipe list page</h1>
      </div>
    );
  }
  
  export default RecipeList;