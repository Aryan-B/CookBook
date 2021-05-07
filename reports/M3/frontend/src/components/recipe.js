import "bootstrap/dist/css/bootstrap.css";
import './list.css';
import Card from 'react-bootstrap/Card';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';


function Recipe({id}) {
    console.log("rendered");
  return (
        <Modal size="lg" aria-labelledby="contained-modal-title-vcenter" centered className="modal">
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {id}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h4>Centered Modal</h4>
        <p>
          Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
          dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta ac
          consectetur ac, vestibulum at eros.
        </p>
      </Modal.Body>
      <Modal.Footer>
        <Button>Close</Button>
      </Modal.Footer>
    </Modal> 
  );
}

export default Recipe;