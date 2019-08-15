#[derive(PartialEq, Eq, Debug)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    pub fn new(val: i32) -> Self {
        ListNode {
            next: None,
            val,
        }
    }
}

// 强行顺序生成的代码反而并不直观，还碰了很多坑
pub fn to_list(vec: Vec<i32>) -> Option<Box<ListNode>> {
    let mut front = ListNode::new(0);
    let mut current = &mut front;
    for &val in vec.iter() {
        current.next = Some(Box::new(ListNode::new(val)));
        current = current.next.as_deref_mut().unwrap()
    }
    return front.next;
}

/*
// 逆向生成的代码 by aylei，较为直观
pub fn to_list(vec: Vec<i32>) -> Option<Box<ListNode>> {
    let mut current = None;
    for &v in vec.iter().rev() {
        let mut node = ListNode::new(v);
        node.next = current;
        current = Some(Box::new(node));
    }
    current
}
*/
