import {useEffect, useState} from 'react';
import axios from 'axios';
import _ from 'lodash';
import "bootstrap/dist/css/bootstrap.css";
import './list.css';
import {Link} from 'react-router-dom';

import {AnimatePresence,motion} from 'framer-motion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import CardDeck from 'react-bootstrap/CardDeck';

function RecipeList(props) {
    const [loaded,setloaded]=useState(false);
    var mitems=[];
    var [combineditems, setCI]=useState([]);
    var [srecipes,setSR] = useState([]);
    const vals=props.location.state;
    let fd= new FormData();
    
    async function setitems(){
        for (let i = 0 ; i < vals.length ; i++) {
            if(vals[i].type!=='string'){
                // console.log(vals[i]);
            fd.append('file'+[i], vals[i]);}
            else{
                mitems.push(vals[i]);
            }
        }
        // console.log(vals);
        return;

    }
    async function fetchMyAPI() {
        
        await axios.post('http://localhost:8080/recognise', fd).then(response=>{
            // console.log(response);
            if(response.status===200){
                _.forEach(response.data,item=>{
                    if(item.hasOwnProperty('type')){
                    mitems.push(item);}
                })
                
                    // console.log('right below');
                    // console.log(mitems);

                    setloaded(true);
                }
                else{
                    console.log('aw snap, failed!');
            }
        }).then(async ()=>{setCI(mitems);});
        

        await axios.post('http://localhost:8080/ingredients', mitems).then(async (response)=>{setSR(response.data); console.log(response.data)});
            // setSR(secondresponse.data);
            // console.log(;
            // return;
    }    

    var mappedItems = (combineditems||[]).filter(function(item){
                // console.log("here");
                // console.log(combineditems);
                if(item.type!=='fstatus'){
                    return item;
                }
            }).map(item => (
                <div className="pad" key={item.name}>
                    <div key={item.name} className="sitems w3-button ">
                    {item.name}
                    </div>
                </div>
              ));


    useEffect(()=>{
          setitems();
          fetchMyAPI();
        // console.log(mitems);
        // fetchRecipe(items);
        console.log("effect has run");
        
        
    },[]);

    useEffect(()=>{
        setCI(mitems);
        console.log(loaded);
        // console.log(combineditems);

    },[]);

    // const Map = [1,2,3,4,5,6,7,8,9,10]
    var listitems = srecipes.map(items=>(
        <div className="pad">
        <Card key={items.id} className="cards">
        <Card.Img variant="top" src={items.image} />
        <Card.Body>
          <Card.Title>{items.title}</Card.Title>
          <Card.Text>
          Likes : {items.likes}
          </Card.Text>
        </Card.Body>
        <div className="cfooter">
        <Card.Footer className="ccfooter">
        <Button className="rmore" onClick={()=>{}} variant="primary">Explore</Button>
        </Card.Footer>
        </div>
      </Card>
      </div>
    ));

//     <div className="item" key={items.id}>
//     <div className="recipeLogo"><Image className="recipeLogo"src= {items.image} fluid></Image></div>
//     <div className="rheading">{items.title}</div>
//     <div className="rinfo">Likes : {items.likes}</div>
//     <div className="rmore" onClick={()=>{}}>Explore</div>
// </div>

  

    return (      
      <motion.div 
      initial={{opacity:0}} 
      animate={{opacity:1}}
      exit={{opacity:0}}
      className="container">
        <h1>Recipe List Page</h1>
      <div className="w3-sidebar w3-bar-block w3-card sidebar">
          <div className="pad"><Link to='/'><Button variant="outline-danger" className='close'> × </Button></Link></div>
      <h3 className="w3-bar-item sh">Analysed Items</h3>
          <div className="itemContainer">{mappedItems}</div>
          </div>

        <CardDeck className= 'recipelist'>
        {listitems} 
        </CardDeck>
      </motion.div>
    );
  }
  
  export default RecipeList;