import React, {useEffect, useState} from 'react';
import {useDropzone} from 'react-dropzone';
import styled from 'styled-components';
import "bootstrap/dist/css/bootstrap.css";
import '../App.css';
import _ from 'lodash';
import {Link} from 'react-router-dom';
import {AnimatePresence,motion} from 'framer-motion'
import ParallaxCard from 'react-parallax-card'
import Tilt from "react-parallax-tilt";
import { Controller, Scene } from 'react-scrollmagic';
import cardimg from '../bg3.jpg'
import ReactPageScroller from 'react-page-scroller';
import sdg from './scroll_downgif.gif'

import ting from './ting.png'
import jeremy from './jeremy.png'
import aryan from './aryan.jpg'
import rushil from './veg.png'

const getColor = (props) => {
  if (props.isDragAccept) {
      return '#00e676';
  }
  if (props.isDragReject) {
      return '#ff1744';
  }
  if (props.isDragActive) {
      return '#2196f3';
  }
  return 'grey';
}

const Container = styled.div`
  margin:auto;
  width:40vw;
  align-items: center;
  padding: 20px;
  border-width: 2px;
  border-radius: 2px;
  border-color: ${props => getColor(props)};
  border-style: dashed;
  background-color: rgba(250, 250, 250,0.2);
  color: white;
  outline: none;
  transition: border .24s ease-in-out;
  margin-bottom:20px;
`;


  


function Dragdrop(props) {
 
  var [files, setFiles] = useState([]);
  var [mfiles, setmFiles] = useState([]);
  let addfield = React.createRef();
 
  const uploadfiles=()=>{
    // console.log(mfiles.concat(files));
    // setFiles([]);
    //   setmFiles([]);
    }

  const DeleteFile = (file)=>{
        files=files.filter(function(ele){ 
        if(ele.name !== file.name)
        {return ele;}
        });
    setFiles(files);
   }

   const DeletemFile = (mfile)=>{
        mfiles=mfiles.filter(function(ele){ 
            if(ele.name !== mfile.name)
                {return ele;}
            });
        setmFiles(mfiles);
    }

    const addtolist = (iname)=>{
        const maunualInput={name:iname,
            type:'string',
        };
        var match=-1;
        mfiles.forEach(function(obj){
            if(obj.name === maunualInput.name){
                match=0;}});
        if(match!==0 && maunualInput.name!==""){    
            mfiles.push(maunualInput);
            mfiles=mfiles.concat([]);
        }
        addfield.current.value="";
        setmFiles(mfiles);
    }

    const arrayUnion = (arr1, arr2, identifier) => {
        const array = [...arr1, ...arr2]
        return _.uniqBy(array, identifier)  
    }

    const {getRootProps,
        getInputProps,
        isDragActive,
        isDragAccept,
        isDragReject} = useDropzone({
        accept: 'image/*',
        onDrop: acceptedFiles => {

        files=arrayUnion(files,acceptedFiles,'name');
        
        setFiles(files.map(file => Object.assign(file, {
            preview: URL.createObjectURL(file)
        })));
        }
    });
  
  var thumbsImg = files.map(file => (
    <div className="thumb"  key={file.name}>
      <div className="thumbInner">
        <img
          src={file.preview}
          className="img" alt="Aw Snap x_x"
        />
      </div>
      <button className="thumbButton" onClick={()=>DeleteFile(file)}>x</button>
    </div>
  ));


  var thumbstxt = mfiles.map(mfile => (
    <div className="thumb" key={mfile.name}>
      <div className="thumbInner">
          <div className="img">{mfile.name}</div>
      </div>
      <button className="thumbButton" onClick={()=>DeletemFile(mfile)}>x</button>
    </div>
  ));


  useEffect(() => () => {
    files.forEach(file => URL.revokeObjectURL(file.preview));
  }, [mfiles,files]);

  var [toggle,setToggle] = useState({isHidden: true});
  var [widgettoggle,setwToggle] = useState({isHidden : (typeof props.location.state)==='undefined'? true : props.location.state});

  return (
    <motion.div 
    initial={{opacity:0}} 
    animate={{opacity:1}}
    exit={{opacity:0}} className="jtron" >
      


      <section className="coverpage"  id={widgettoggle.isHidden ? 'slideup':'slidedown'}>
      <div onClick={()=>{setToggle((prevState)=>({isHidden: !prevState.isHidden}))}}>
        
      <Tilt
      className="parallax-effect-glare-scale"
      perspective={1000}
      scale={1.0}
      gyroscope={true}
      glareEnable={true}
      glareMaxOpacity={0.2} 
      glareReverse={true}
      glarePosition={'all'}
      >
      <div className="inner-element" >
        <div className="pad">
          <h1>Welcome To CookBook</h1>
          </div>
          <div  style={{fontSize:'0.5em',textAlign:'center',padding:'20px'}}>
          Your personalised cooking app. This app uses AI to recognise your "non-identifiable" kitchen ingredient and gives a recipe that can be made using those items
          </div>
          
      </div>
      
    </Tilt>
    </div>
      <div className="gmsidebar" id={toggle.isHidden ? 'gmsidebar-in':'gmsidebar-out'}>
      <div style={{width:"100%",textAlign:"center",background:"rgb(14, 163, 231)",padding:"10px",top:"0",fontSize:"2em"}}>Meet the Team</div>
      <div className="gm" style={{background:'url('+aryan+')',backgroundSize:"cover",backgroundPosition:"center",backgroundRepeat:"no-repeat"}}>
              <div className="gmname" >Aryan</div>
        </div>
        <div className="gm" style={{background:'url('+jeremy+')',backgroundSize:"cover",backgroundPosition:"center",backgroundRepeat:"no-repeat"}}>
              <div className="gmname">Jeremy</div>
        </div>
        <div className="gm" style={{background:'url('+rushil+')',backgroundSize:"cover",backgroundPosition:"center",backgroundRepeat:"no-repeat"}}>
              <div className="gmname">Rushil</div>
        </div>
        <div className="gm" style={{background:'url('+ting+')',backgroundSize:"cover",backgroundPosition:"center",backgroundRepeat:"no-repeat"}}>
              <div className="gmname">Ting</div>
        </div>
        
      </div>
      <div className="scrolldown" id={toggle.isHidden ? 'fadein':'fadeout'} 
      onClick={()=>{setwToggle((prevState)=>({isHidden: !prevState.isHidden}));setToggle((prevState)=>({isHidden: !prevState.isHidden}))}} style={{cursor:"pointer"}}> 
        <img src={sdg} style={{height:'50px',width:'50px'}}/> Scroll down<img src={sdg} style={{height:'50px',width:'50px'}}/>
      </div>
      </section>


    <section className="App" id={widgettoggle.isHidden ? 'wfadein':'wfadeout'}>
      <div className="container">
      <div className="w3-container ">
        <h1 className='header'>CookBook</h1>
      </div>
        <div className='addform'>
            <div className="inputbox"><input ref={addfield} onKeyPress={(ev) => { if (ev.key === 'Enter') {
                addtolist(addfield.current.value); ev.preventDefault(); }}} type="text" className="AddIngredientsText"/></div>
            <button className="AddButton" onClick={()=>addtolist(addfield.current.value)}>Add</button>
        </div>
        <Container {...getRootProps({isDragActive, isDragAccept, isDragReject})}>
            <input {...getInputProps()} />
            <p>Drag 'n' drop some files here, or click to select files</p>
        </Container>
        <div className="thumbsContainer">
            {thumbsImg}
            {thumbstxt}
        </div>
        <div className='upload thumbsContainer'><Link to={{pathname: '/list', state: mfiles.concat(files)}}><button className="AddButton" onClick={()=>uploadfiles()}>Upload</button></Link></div>
        </div>
        <div className="scrollup " > 
        <div className="sitems1" onClick={()=>{setwToggle((prevState)=>({isHidden: !prevState.isHidden}))}} style={{cursor:"pointer"}}> Back to top</div>
      </div>
        </section>
        
    </motion.div>

  );
}

export default Dragdrop;
