import {useEffect, useState} from 'react';
import axios from 'axios';
import _ from 'lodash';
import "bootstrap/dist/css/bootstrap.css";
import {Link} from 'react-router-dom';
import {AnimatePresence,motion} from 'framer-motion';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';

import Button from 'react-bootstrap/Button';
import Badge from 'react-bootstrap/Badge';

import CardDeck from 'react-bootstrap/CardDeck';
import Recipe from './recipe';
import Modal from 'react-bootstrap/Modal';
import './list.css';
import veg from './veg.png';
import nveg from './nveg.png';


function RecipeList(props) {
    const [loaded,setloaded]=useState(false);
    var mitems=[];
    var [combineditems, setCI]=useState([]);
    var [srecipes,setSR] = useState([]);


    const vals=props.location.state;
    let fd= new FormData();

    const [show, setShow] = useState(false);
    const handleClose=() => setShow(false);
    const handleShow=() => setShow(true);

    const [showModal, setShowModal] = useState(false);
    const [modalInfo, setModalInfo] = useState({
    'analyzedInstructions': [{'name': '',
                           'steps': [{'step': ''}]}],
    'cuisines': [],
    'dishTypes': [],
    'extendedIngredients': [{'originalString': ''}],
    'id': 0,
    'image': '',
    'readyInMinutes': 0,
    'servings': 0,
    'sourceUrl': '',
    'title': '',
    'vegetarian': false,
    'winePairing': {'pairedWines': ['']}
    });
    const toggletf = ()=>{
        setShowModal(handleShow);
    }

    const ModalContent = () => {
        return(
            <Modal  show={show} onHide={handleClose}  dialogClassName="modal-90w" aria-labelledby="example-custom-modal-styling-title" centered id="modal">
                <div className="modalwh">
            <Modal.Header className="heading">
            <Modal.Title id="contained-modal-title-vcenter">
                {modalInfo.title} 
            </Modal.Title><div className="pad"><Button onClick={handleClose} variant="outline-danger" className='close modalclose'> × </Button></div>
            </Modal.Header>
            <Modal.Body id="mbody">

            <div className="w3-sidebar w3-bar-block rsidebar">
                <div className="pad parent">
                    <Image fluid src={modalInfo.image} className="recipeImg"/>
                    <div className="pad veg">
                        {modalInfo.vegetarian===true ? <Image className="close" src={veg}/>:<Image src={nveg} className="close"/>}
                    </div>
                </div>
                <div className="w3-bar-item">Ready In : <Badge  >
                    <div  className="sitems w3-button ">{modalInfo.readyInMinutes} minutes</div></Badge>
                </div>
                <div className="w3-bar-item">Serving Size : <Badge  >
                    <div  className="sitems w3-button ">{modalInfo.servings}</div></Badge>
                </div>
                {cuisines.length===0 ? null: <div className="w3-bar-item">Cuisine : {cuisines} </div>}
                {winepairing.length===0 ? null: <div className="w3-bar-item">Wine Pairing : {winepairing}</div>}
            </div>
            <div className="ingredient-area" id= "content-header"><h4>Ingredients : </h4> </div>
            <ul className="ingredient-area">{ingredientlist}</ul>
            <div className="instruction-area" id= "content-header"><h4>Instructions : </h4> </div>
            <ul className="instruction-area">{instructionlist}</ul>

            </Modal.Body>
        
            </div>
            </Modal> 
        );
    }
    // modalInfo.winePairing.pairedWines||
    var winepairing=modalInfo.winePairing.pairedWines.map(function(val, index){    
        return(
            <Badge  key={val}>
                <div key={val} className="sitems w3-button ">
                    {val}
                </div>
            </Badge>
      );}
      );

        
  var cuisines=(modalInfo.cuisines).map(function(val, index){    
    return(
        <Badge  key={val}>
            <div key={val} className="sitems w3-button ">
                 {val}
            </div>
        </Badge>
    );});
        
        
  var ingredientlist=(modalInfo.extendedIngredients).map(function(val, index){    
    return(
        <li className="pad" key={val}>
            <div key={val.originalString} className="sitems w3-button ">
                 {val.originalString}
            </div>
        </li>
    );});
    
    var instructionlist= (modalInfo.analyzedInstructions[0].steps).map(function(val, index){    
        return(
            <li key={val.step}>
                     {val.step}
            </li>
        );});
        


    async function setitems(){
        for (let i = 0 ; i < vals.length ; i++) {
            if(vals[i].type!=='string'){
            fd.append('file'+[i], vals[i]);}
            else{
                mitems.push(vals[i]);
            }
        }
        return;

    }
    async function fetchMyAPI() {
        
        await axios.post('http://localhost:8080/recognise', fd).then(response=>{
            if(response.status===200){
                _.forEach(response.data,item=>{
                    if(item.hasOwnProperty('type')){
                    mitems.push(item);}
                })
                    setloaded(true);
                }
                else{
                    console.log('aw snap, failed!');
            }
        }).then( async ()=>{setCI(mitems);});
        await axios.post('http://localhost:8080/ingredients', mitems).then(async (response)=>{setSR(response.data); console.log(response.data)});
    }    

    var mappedItems = (combineditems||[]).filter(function(item){
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

    async function recipePage(id){
        console.log(id);
        await axios.post('http://localhost:8080/recipe', {'id':id}).then(async (response)=>{setModalInfo(response.data); console.log(response.data)});
        toggletf();
    }

    useEffect(()=>{
        setitems();
        fetchMyAPI();
        setCI(mitems);
        console.log("effect has run");
    },[]);

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
        <Button className="rmore" onClick={()=>recipePage(items.id)} variant="primary">Explore</Button>
        </Card.Footer>
        </div>
      </Card>
      </div>
    ));




  

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
      {show?  < ModalContent/> : null}

      </motion.div>
    );
  }
  
  export default RecipeList;