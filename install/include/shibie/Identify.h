// Generated by gencpp from file shibie/Identify.msg
// DO NOT EDIT!


#ifndef SHIBIE_MESSAGE_IDENTIFY_H
#define SHIBIE_MESSAGE_IDENTIFY_H

#include <ros/service_traits.h>


#include <shibie/IdentifyRequest.h>
#include <shibie/IdentifyResponse.h>


namespace shibie
{

struct Identify
{

typedef IdentifyRequest Request;
typedef IdentifyResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct Identify
} // namespace shibie


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::shibie::Identify > {
  static const char* value()
  {
    return "86f4e91a6ab25c36871755e93aece959";
  }

  static const char* value(const ::shibie::Identify&) { return value(); }
};

template<>
struct DataType< ::shibie::Identify > {
  static const char* value()
  {
    return "shibie/Identify";
  }

  static const char* value(const ::shibie::Identify&) { return value(); }
};


// service_traits::MD5Sum< ::shibie::IdentifyRequest> should match
// service_traits::MD5Sum< ::shibie::Identify >
template<>
struct MD5Sum< ::shibie::IdentifyRequest>
{
  static const char* value()
  {
    return MD5Sum< ::shibie::Identify >::value();
  }
  static const char* value(const ::shibie::IdentifyRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::shibie::IdentifyRequest> should match
// service_traits::DataType< ::shibie::Identify >
template<>
struct DataType< ::shibie::IdentifyRequest>
{
  static const char* value()
  {
    return DataType< ::shibie::Identify >::value();
  }
  static const char* value(const ::shibie::IdentifyRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::shibie::IdentifyResponse> should match
// service_traits::MD5Sum< ::shibie::Identify >
template<>
struct MD5Sum< ::shibie::IdentifyResponse>
{
  static const char* value()
  {
    return MD5Sum< ::shibie::Identify >::value();
  }
  static const char* value(const ::shibie::IdentifyResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::shibie::IdentifyResponse> should match
// service_traits::DataType< ::shibie::Identify >
template<>
struct DataType< ::shibie::IdentifyResponse>
{
  static const char* value()
  {
    return DataType< ::shibie::Identify >::value();
  }
  static const char* value(const ::shibie::IdentifyResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // SHIBIE_MESSAGE_IDENTIFY_H
