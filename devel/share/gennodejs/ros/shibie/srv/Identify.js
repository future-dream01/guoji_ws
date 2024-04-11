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
      this.back = null;
    }
    else {
      if (initObj.hasOwnProperty('back')) {
        this.back = initObj.back
      }
      else {
        this.back = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type IdentifyResponse
    // Serialize message field [back]
    bufferOffset = _serializer.string(obj.back, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type IdentifyResponse
    let len;
    let data = new IdentifyResponse(null);
    // Deserialize message field [back]
    data.back = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.back);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'shibie/IdentifyResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c4a1d3ec3f5c241f65fed707d363d25e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string back
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new IdentifyResponse(null);
    if (msg.back !== undefined) {
      resolved.back = msg.back;
    }
    else {
      resolved.back = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: IdentifyRequest,
  Response: IdentifyResponse,
  md5sum() { return '7debc7ecb9cc5cb9fe2af4ff555737b7'; },
  datatype() { return 'shibie/Identify'; }
};
