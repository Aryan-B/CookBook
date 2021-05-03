import {useEffect, useState} from 'react';
import axios from 'axios';
import './list.css';
import _ from 'lodash';


function RecipeList(props) {
    const [loaded,setloaded]=useState(false);
    var [items,setMI]=useState([]);

    const vals=props.location.state;
    async function fetchMyAPI() {
        let fd= new FormData();
        
          
        for (let i = 0 ; i < vals.length ; i++) {
            if(vals[i].type!=='string'){
                // console.log(vals[i]);
            fd.append('file'+[i], vals[i]);}
            else{
                setMI(oldArray => [...oldArray, vals[i]]);
            }
        }
        const response= await axios.post('http://localhost:8080/recognise', fd);
        if(response.data.name==='Success'){
            setMI(prev=>[...prev, response.data]);
                    // console.log(typeof(itemsTBD));
                    // console.log(itemsTBD);

                  
                console.log('success');
                setloaded(true);
            }
            else{
                console.log('aw snap, failed!');
        };    
    }

    var mappedItems = items.filter(function(item){
        // console.log(items);
        if(!_.has(item, 'result')){
            // console.log(itemsTBD);
            return item;
        }
    }).map(item => (
        <div key={item.name}>
            <div>{item.name}</div>
        </div>
      ));

    useEffect(()=>{
        fetchMyAPI();
        // console.log("effect has run");
        
    },[]);

    

    return (      
      <div className="App">
        <h1>Recipe list page</h1>
      {mappedItems}

      </div>
    );
  }
  
  export default RecipeList;