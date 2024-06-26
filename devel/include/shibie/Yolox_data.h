// Generated by gencpp from file shibie/Yolox_data.msg
// DO NOT EDIT!


#ifndef SHIBIE_MESSAGE_YOLOX_DATA_H
#define SHIBIE_MESSAGE_YOLOX_DATA_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace shibie
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





  typedef boost::shared_ptr< ::shibie::Yolox_data_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::shibie::Yolox_data_<ContainerAllocator> const> ConstPtr;

}; // struct Yolox_data_

typedef ::shibie::Yolox_data_<std::allocator<void> > Yolox_data;

typedef boost::shared_ptr< ::shibie::Yolox_data > Yolox_dataPtr;
typedef boost::shared_ptr< ::shibie::Yolox_data const> Yolox_dataConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::shibie::Yolox_data_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::shibie::Yolox_data_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::shibie::Yolox_data_<ContainerAllocator1> & lhs, const ::shibie::Yolox_data_<ContainerAllocator2> & rhs)
{
  return lhs.target == rhs.target &&
    lhs.x_p == rhs.x_p &&
    lhs.y_p == rhs.y_p;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::shibie::Yolox_data_<ContainerAllocator1> & lhs, const ::shibie::Yolox_data_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace shibie

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::shibie::Yolox_data_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::shibie::Yolox_data_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::shibie::Yolox_data_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::shibie::Yolox_data_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::shibie::Yolox_data_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::shibie::Yolox_data_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::shibie::Yolox_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dd8ae1831add5d55430f288fc3367194";
  }

  static const char* value(const ::shibie::Yolox_data_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xdd8ae1831add5d55ULL;
  static const uint64_t static_value2 = 0x430f288fc3367194ULL;
};

template<class ContainerAllocator>
struct DataType< ::shibie::Yolox_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "shibie/Yolox_data";
  }

  static const char* value(const ::shibie::Yolox_data_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::shibie::Yolox_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 target\n"
"float32 x_p\n"
"float32 y_p\n"
;
  }

  static const char* value(const ::shibie::Yolox_data_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::shibie::Yolox_data_<ContainerAllocator> >
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
struct Printer< ::shibie::Yolox_data_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::shibie::Yolox_data_<ContainerAllocator>& v)
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

#endif // SHIBIE_MESSAGE_YOLOX_DATA_H
