extern crate gtrie;
extern crate libc;

use libc::{c_char, uint32_t};
use std::ffi::CStr;


fn ptr_to_str<'a>(ptr: *const c_char) -> &'a str {
    let c_str = unsafe {
        assert!(!ptr.is_null());
        CStr::from_ptr(ptr)
    };

    c_str.to_str().unwrap()
}


fn ptr_to_string(ptr: *const c_char) -> String {
    String::from(ptr_to_str(ptr))
}


#[no_mangle]
pub extern fn dictionary_new() -> *mut gtrie::Trie<char, String> {
    Box::into_raw(Box::new(gtrie::Trie::<char, String>::new()))
}


#[no_mangle]
pub extern fn dictionary_free(ptr: *mut gtrie::Trie<char, String>) {
    if ptr.is_null() {
        return;
    }
    unsafe { Box::from_raw(ptr); }
}


#[no_mangle]
pub extern fn add_keyword(
    dictionary_ptr: *mut gtrie::Trie<char, String>,
    keyword_ptr: *const c_char,
    synonim_ptr: *const c_char,
) {
    let dictionary = unsafe {
        assert!(!dictionary_ptr.is_null());
        &mut *dictionary_ptr
    };

    dictionary.insert(ptr_to_str(keyword_ptr).chars(), ptr_to_string(synonim_ptr));
}


#[no_mangle]
pub extern fn contains_keyword(
    dictionary_ptr: *mut gtrie::Trie<char, String>,
    keyword_ptr: *const c_char,
) -> bool {
    let dictionary = unsafe {
        assert!(!dictionary_ptr.is_null());
        &mut *dictionary_ptr
    };

    dictionary.contains_key(ptr_to_str(keyword_ptr).chars())
}
