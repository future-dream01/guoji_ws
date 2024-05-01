// Generated by gencpp from file main/Yolox_data.msg
// DO NOT EDIT!


#ifndef MAIN_MESSAGE_YOLOX_DATA_H
#define MAIN_MESSAGE_YOLOX_DATA_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace main
{
template <class ContainerAllocator>
struct Yolox_data_
{
  typedef Yolox_data_<ContainerAllocator> Type;

  Yolox_data_()
    : target(0)
    , x_p(0.0)
    , y_p(0.0)  {
    }
  Yolox_data_(const ContainerAllocator& _alloc)
    : target(0)
    , x_p(0.0)
    , y_p(0.0)  {
  (void)_alloc;
    }



   typedef uint8_t _target_type;
  _target_type target;

   typedef float _x_p_type;
  _x_p_type x_p;

   typedef float _y_p_type;
  _y_p_type y_p;





  typedef boost::shared_ptr< ::main::Yolox_data_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::main::Yolox_data_<ContainerAllocator> const> ConstPtr;

}; // struct Yolox_data_

typedef ::main::Yolox_data_<std::allocator<void> > Yolox_data;

typedef boost::shared_ptr< ::main::Yolox_data > Yolox_dataPtr;
typedef boost::shared_ptr< ::main::Yolox_data const> Yolox_dataConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::main::Yolox_data_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::main::Yolox_data_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::main::Yolox_data_<ContainerAllocator1> & lhs, const ::main::Yolox_data_<ContainerAllocator2> & rhs)
{
  return lhs.target == rhs.target &&
    lhs.x_p == rhs.x_p &&
    lhs.y_p == rhs.y_p;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::main::Yolox_data_<ContainerAllocator1> & lhs, const ::main::Yolox_data_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace main

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::main::Yolox_data_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::main::Yolox_data_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::main::Yolox_data_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::main::Yolox_data_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::main::Yolox_data_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::main::Yolox_data_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::main::Yolox_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dd8ae1831add5d55430f288fc3367194";
  }

  static const char* value(const ::main::Yolox_data_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xdd8ae1831add5d55ULL;
  static const uint64_t static_value2 = 0x430f288fc3367194ULL;
};

template<class ContainerAllocator>
struct DataType< ::main::Yolox_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "main/Yolox_data";
  }

  static const char* value(const ::main::Yolox_data_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::main::Yolox_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 target\n"
"float32 x_p\n"
"float32 y_p\n"
;
  }

  static const char* value(const ::main::Yolox_data_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::main::Yolox_data_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.target);
      stream.next(m.x_p);
      stream.next(m.y_p);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Yolox_data_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::main::Yolox_data_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::main::Yolox_data_<ContainerAllocator>& v)
  {
    s << indent << "target: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.target);
    s << indent << "x_p: ";
    Printer<float>::stream(s, indent + "  ", v.x_p);
    s << indent << "y_p: ";
    Printer<float>::stream(s, indent + "  ", v.y_p);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MAIN_MESSAGE_YOLOX_DATA_H
