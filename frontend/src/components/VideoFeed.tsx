import Webcam from 'react-webcam';
import React from 'react';

class VideoFeed extends React.Component {
    render() {
        const videoConstraints = {
            facingMode: "user"
        };

        return <Webcam videoConstraints={videoConstraints} mirrored={true} />;
    }
}

export default VideoFeed;