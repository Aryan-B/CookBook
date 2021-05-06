import React, {useEffect, useState} from 'react';
import {useDropzone} from 'react-dropzone';
import styled from 'styled-components';
import '../App.css';
import _ from 'lodash';
import {Link} from 'react-router-dom';
import {AnimatePresence,motion} from 'framer-motion'


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


  


function Dragdrop() {
 
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

  return (
    <motion.div 
    initial={{opacity:0}} 
    animate={{opacity:1}}
    exit={{opacity:0}}
    className="container">
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
    </motion.div>
  );
}

export default Dragdrop;
