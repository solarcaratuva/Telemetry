import Webcam from 'react-webcam';
import React from 'react';

class VideoFeed extends React.Component {
    render() {
        const videoConstraints = {
            width: 975,
            height: 500,
            facingMode: "user"
        };

        return <Webcam videoConstraints={videoConstraints} mirrored={true} />;
    }
}

export default VideoFeed;