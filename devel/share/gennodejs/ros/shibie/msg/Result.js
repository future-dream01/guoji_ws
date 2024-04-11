// Auto-generated. Do not edit!

// (in-package shibie.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Result {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.target = null;
      this.x_p = null;
      this.y_p = null;
    }
    else {
      if (initObj.hasOwnProperty('target')) {
        this.target = initObj.target
      }
      else {
        this.target = 0;
      }
      if (initObj.hasOwnProperty('x_p')) {
        this.x_p = initObj.x_p
      }
      else {
        this.x_p = 0.0;
      }
      if (initObj.hasOwnProperty('y_p')) {
        this.y_p = initObj.y_p
      }
      else {
        this.y_p = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Result
    // Serialize message field [target]
    bufferOffset = _serializer.uint8(obj.target, buffer, bufferOffset);
    // Serialize message field [x_p]
    bufferOffset = _serializer.float32(obj.x_p, buffer, bufferOffset);
    // Serialize message field [y_p]
    bufferOffset = _serializer.float32(obj.y_p, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Result
    let len;
    let data = new Result(null);
    // Deserialize message field [target]
    data.target = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [x_p]
    data.x_p = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [y_p]
    data.y_p = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 9;
  }

  static datatype() {
    // Returns string type for a message object
    return 'shibie/Result';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'dd8ae1831add5d55430f288fc3367194';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 target
    float32 x_p
    float32 y_p
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Result(null);
    if (msg.target !== undefined) {
      resolved.target = msg.target;
    }
    else {
      resolved.target = 0
    }

    if (msg.x_p !== undefined) {
      resolved.x_p = msg.x_p;
    }
    else {
      resolved.x_p = 0.0
    }

    if (msg.y_p !== undefined) {
      resolved.y_p = msg.y_p;
    }
    else {
      resolved.y_p = 0.0
    }

    return resolved;
    }
};

module.exports = Result;
