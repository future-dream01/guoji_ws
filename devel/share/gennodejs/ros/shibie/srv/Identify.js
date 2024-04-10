// Auto-generated. Do not edit!

// (in-package shibie.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class IdentifyRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.call = null;
    }
    else {
      if (initObj.hasOwnProperty('call')) {
        this.call = initObj.call
      }
      else {
        this.call = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type IdentifyRequest
    // Serialize message field [call]
    bufferOffset = _serializer.string(obj.call, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type IdentifyRequest
    let len;
    let data = new IdentifyRequest(null);
    // Deserialize message field [call]
    data.call = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.call);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'shibie/IdentifyRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e3215900da2c21797ec453ce12acd7b3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string call
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new IdentifyRequest(null);
    if (msg.call !== undefined) {
      resolved.call = msg.call;
    }
    else {
      resolved.call = ''
    }

    return resolved;
    }
};

class IdentifyResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.target = null;
      this.x = null;
      this.y = null;
    }
    else {
      if (initObj.hasOwnProperty('target')) {
        this.target = initObj.target
      }
      else {
        this.target = 0;
      }
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = 0;
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type IdentifyResponse
    // Serialize message field [target]
    bufferOffset = _serializer.uint8(obj.target, buffer, bufferOffset);
    // Serialize message field [x]
    bufferOffset = _serializer.int64(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.int64(obj.y, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type IdentifyResponse
    let len;
    let data = new IdentifyResponse(null);
    // Deserialize message field [target]
    data.target = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [x]
    data.x = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.int64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 17;
  }

  static datatype() {
    // Returns string type for a service object
    return 'shibie/IdentifyResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '15449436763f6557c2e68c9c70afc48d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 target
    int64 x
    int64 y
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new IdentifyResponse(null);
    if (msg.target !== undefined) {
      resolved.target = msg.target;
    }
    else {
      resolved.target = 0
    }

    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = 0
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = 0
    }

    return resolved;
    }
};

module.exports = {
  Request: IdentifyRequest,
  Response: IdentifyResponse,
  md5sum() { return '86f4e91a6ab25c36871755e93aece959'; },
  datatype() { return 'shibie/Identify'; }
};
