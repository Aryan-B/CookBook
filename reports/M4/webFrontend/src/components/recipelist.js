import {useEffect, useState} from 'react';
import axios from 'axios';
import _ from 'lodash';
import "bootstrap/dist/css/bootstrap.css";
import {Link} from 'react-router-dom';
import {motion} from 'framer-motion';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';

import Button from 'react-bootstrap/Button';
import Badge from 'react-bootstrap/Badge';

import CardDeck from 'react-bootstrap/CardDeck';
import Modal from 'react-bootstrap/Modal';
import './list.css';
import veg from './veg.png';
import nveg from './nveg.png';
import * as uuid  from 'uuid';
import loader from './loader.gif'
function RecipeList(props) {
    var [sidebarloaded,setSBloaded]=useState(false);
    var [listloaded,setLloaded]=useState(false);
    var [recipeloaded,setRloaded]=useState(false);


    var mitems=[];
    var [combineditems, setCI]=useState([]);
    var [srecipes,setSR] = useState([]);


    const vals=props.location.state;
    let fd= new FormData();

    const [show, setShow] = useState(false);
    const handleClose=() => 
    {   setRloaded(false);
        setShow(false);}
    const handleShow=() => setShow(true);

    const [modalInfo, setModalInfo] = useState({
    'analyzedInstructions': [{'name': '',
                           'steps': []}],
    'cuisines': [],
    'dishTypes': [],
    'extendedIngredients': [],
    'id': 0,
    'image': '',
    'readyInMinutes': 0,
    'servings': 0,
    'sourceUrl': '',
    'title': '',
    'vegetarian': false,
    'winePairing': {'pairedWines': []}
    });


    const url='http://18.221.82.143:8080';

    var Winepairing= ()=>{
        if((_.has(modalInfo.winePairing,'pairedWines') === true)){
            return modalInfo.winePairing.pairedWines && modalInfo.winePairing.pairedWines.map(function(val, index){    
                return(
                    <Badge  key={uuid.v4()} style={{textDecoration:'none',cursor:'auto'}}>
                        <div key={uuid.v4()} className="sitems w3-button " style={{textDecoration:'none',cursor:'auto'}}>
                            {val}
                        </div>
                    </Badge>
                    );
                });}
        return null;
    }
        
    var Cuisines=()=>{
        if(_.has(modalInfo,'cuisines')){
            return modalInfo.cuisines.map(function(val, index){    
                return(
                    <Badge  key={uuid.v4()} style={{textDecoration:'none',cursor:'default'}}>
                        <div key={uuid.v4()} className="sitems w3-button " style={{textDecoration:'none',cursor:'auto'}}>
                            {val}
                        </div>
                    </Badge>
            );});}
    return null;
    }

    var Linkurl=()=>{
        if(_.has(modalInfo,'sourceUrl')){
            return (
                    <a href={modalInfo.sourceUrl} target="_blank"><Badge  key={uuid.v4()} style={{textDecoration:'none',cursor:'auto'}}>
                        <div key={uuid.v4() } className="sitems w3-button " >
                            Source ↗
                        </div>
                    </Badge>
                    </a>
            );}
    return null;
    }
        
        
    var Ingredientlist=()=>{
        if(_.has(modalInfo,'extendedIngredients')){
            return modalInfo.extendedIngredients.map(function(val, index){    
                return(
                    <li className="pad" key={uuid.v4()} style={{textDecoration:'none',cursor:'auto'}}>
                        <div key={uuid.v4()} className="sitems w3-button" style={{textDecoration:'none',cursor:'auto'}}>
                            {val.originalString}
                        </div>
                    </li>
            );});}
        return (
            <li className="pad" key={uuid.v4()}>
                <div key={uuid.v4()} className="sitems w3-button" style={{textDecoration:'none',cursor:'auto'}}>
                    No ingredients were provided by Spoonacular API
                </div>
            </li>
    );}
    
    var Instructionlist= ()=>{
        if(_.has(modalInfo,'analyzedInstructions')&&( modalInfo.analyzedInstructions.length!==0)){
            return modalInfo.analyzedInstructions[0].steps.map(function(val, index){    
                return(
                    <li key={uuid.v4()}>
                            {val.step}
                    </li>
        );});}
        return (
            <li key={uuid.v4()}>
                     No Instructions were provided by Spoonacular API
            </li>
    );}

    var mappedItems = (combineditems||[]).filter(function(item){
        if(item.type!=='fstatus'){
            return item;
        }
        return null;
        }).map(item => (
            <div className="pad" key={uuid.v4()}>
                <div key={uuid.v4()} className="sitems w3-button ">
                {item.name}
                </div>
            </div>
    ));
    
    async function setitems(){
        for (let i = 0 ; i < vals.length ; i++) {
            if(vals[i].type!=='string'){
                fd.append('file'+[i], vals[i]);}
            else{
                mitems.push(vals[i]);
            }
        }
        return null;
    }

    async function fetchMyAPI() {
        await axios.post(url+'/recognise', fd).then(response=>{
            if(response.status===200){
                _.forEach(response.data,item=>{
                    if(item.hasOwnProperty('type')){
                    mitems.push(item);}
                });}
            else{
                console.log('aw snap, failed!');
            }})
        .then( async ()=>{setCI(mitems);setSBloaded(true);});
        
        await axios.post(url+'/ingredients', mitems)
        .then(async (response)=>{
            setSR(response.data); 
            setLloaded(true);
            console.log(response.data);
        });
    }    

    async function recipePage(id){
        console.log(id);
        setModalInfo({});
        handleShow();
        await axios.post(url+'/recipe', {'id':id})
        .then(async (response)=>{
            setModalInfo(response.data); 
            console.log(response.data); 
            setRloaded(true)});
    }

    var listitems = srecipes.map(items=>(
        <div className="pad" key={uuid.v4()}>
            <Card key={uuid.v4()} className="cards">
                <Card.Img variant="top" src={items.image} />
                <Card.Body>
                    <Card.Title>{items.title}</Card.Title>
                    <Card.Text>Likes : {items.likes}</Card.Text>
                </Card.Body>
                <div className="cfooter">
                    <Card.Footer className="ccfooter">
                        <Button className="rmore" onClick={()=>{recipePage(items.id)}} variant="primary">Explore</Button>
                    </Card.Footer>
                </div>
            </Card>
        </div>
    ));

    const ModalContent = () => {
        return(
            <Modal show={show}  onHide={handleClose} dialogClassName="modal-90w" aria-labelledby="example-custom-modal-styling-title" centered id="modal">
                <div className="sloader" id={recipeloaded? 'sidebarloaded':'sidebarloading'} style={{position:'absolute'}}>
                    <div className="preloader">
                        <img src={loader} style={{height:"80px",width:"80px"}} alt="woops"/>
                        <div style={{color:"white"}}>Fetching Recipe Info ...</div>
                    </div>
                </div>
                <div className="modalwh">
                    <div className="heading">
                            {modalInfo.title} 
                        <div className="pad">
                            <Button onClick={handleClose} variant="outline-danger" className=' modalclose close '> × </Button>
                        </div>
                    </div>
                
                    <div id="mbody">
                        <div className="rsidebar">
                            <div className="pad parent">
                                <Image fluid src={modalInfo.image} className="recipeImg"/>
                                <div className="pad veg">
                                    {modalInfo.vegetarian===true ? <Image className="close" src={veg}/>:<Image src={nveg} className="close"/>}
                                </div>
                            </div>
                            <div className="pad">
                                <div className="w3-bar-item">Ready In : <Badge  style={{textDecoration:'none',cursor:'auto'}}>
                                    <div  className="sitems w3-button " style={{textDecoration:'none',cursor:'auto'}}>{modalInfo.readyInMinutes} minutes</div></Badge>
                                </div>
                                <div className="w3-bar-item">Serving Size : <Badge  >
                                    <div style={{textDecoration:'none',cursor:'auto'}} className="sitems w3-button ">{modalInfo.servings}</div></Badge>
                                </div>
                                {((_.has(modalInfo,'cuisines') === true) && (modalInfo.cuisines.length!==0)) ? <div className="w3-bar-item">Cuisine : <Cuisines/> </div>:null}
                                {((_.has(modalInfo.winePairing,'pairedWines') === true) && (modalInfo.winePairing.pairedWines.length!==0))?<div className="w3-bar-item">Wine Pairing : <Winepairing/></div>:null}
                                {((_.has(modalInfo,'sourceUrl') === true) && (modalInfo.sourceUrl!==undefined)) ? <div className="w3-bar-item">Link : <Linkurl/> </div>:null}

                            </div>
                        </div>
                        <div className="content-area">
                                <h4 id= "content-header">Ingredients : </h4> 
                            <div className="ingredient-area ">

                                    <div className="listed"><ul style={{listStyleType:'none'}}><Ingredientlist/></ul></div>
                            </div>
                                <h4 id= "content-header">Instructions : </h4>
                            <div className="instruction-area">

                                <div className="listed2"><ul style={{listStyleType:'decimal'}}><Instructionlist/></ul></div>
                            </div>
                        </div>
                    </div>
                </div>
            </Modal> 
        );
    }

    useEffect(()=>{
        setitems();
        fetchMyAPI();
        setCI(mitems);
        console.log("effect has run");
    },[]);

    return (      
      <motion.div 
        initial={{opacity:0}} 
        animate={{opacity:1}}
        exit={{opacity:0}}
        className="container2">
            <div className="hrecipes">🍉 Recipes 🍕</div>
            <div className="w3-sidebar w3-bar-block w3-card sidebar" >
                <div className="sloader" id={sidebarloaded? 'sidebarloaded':'sidebarloading'}>
                    <div className="preloader">
                        <img src={loader} style={{height:"80px",width:"80px"}} alt="woops"/>
                        <div>Detecting Items ...</div>
                    </div>
                </div>
            <div className="pad">
                <Link to={{pathname: '/', state: false}}>
                    <Button variant="outline-danger" className='close'> × </Button>
                </Link></div>
                <h3 className="w3-bar-item sh">Analysed Items</h3>
                <div className="itemContainer">{mappedItems}</div>
            </div>
            
            <CardDeck className= 'recipelist' >
                <div className="rloader" id={listloaded? 'sidebarloaded':'sidebarloading'}>
                    <div className="preloader">
                        <img src={loader} style={{height:"80px",width:"80px"}} alt="woops"/>
                        <div id={sidebarloaded ? 'rbarloaded':'rbarloading'}>Detecting Items ...</div>
                        <div id={sidebarloaded?  listloaded ? 'rbarloaded': 'rbarloading':'rbarloaded'}>Fetching Recipes ...</div>
                    </div>
                </div>
                {listitems}
            </CardDeck>
            < ModalContent/>
      </motion.div>
    );
  }
  
export default RecipeList;