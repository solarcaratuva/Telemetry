
import React from 'react'


interface Props {
    value: number;
    max: number;
    
  }

const Progress_bar: React.FC<Props> = ({ value, max}) => {
     
    const containerStyles = {
        height: 20,
        width: '75%',
        backgroundColor: "#e0e0de",
        background: 'linear-gradient(to right, gray 0%, gray 50%, green 50%, green 70%, gray 70%)',
        borderRadius: 50,
        margin: 50
      }
    
      const fillerStyles = {
        height: '100%',
        width: `${value/max*100}%`,
        backgroundColor: 'red',
        //background: 'linear-gradient(to right, #430089, #82ffa1)',
        borderRadius: 'inherit',
        //textAlign: 'right'
      }
    
      const labelStyles = {
        padding: 5,
        color: 'white',
        fontWeight: 'bold'
      }

   
        
    return (
        <div style = {containerStyles}>
            
          <div style = {fillerStyles}>
            
            <span style={labelStyles}>{`${value/max*100}%`}</span>
            
          </div>
          
        </div>
      );
};
  
export default Progress_bar;