/**
 * [2] Add Two Numbers
 *
 * You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
 * You may assume the two numbers do not contain any leading zero, except the number 0 itself.
 * Example:
 * 
 * Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
 * Output: 7 -> 0 -> 8
 * Explanation: 342 + 465 = 807.
 * 
 */

pub struct Solution {}
use super::utils::linked_list::{ListNode, to_list};
use std::borrow::BorrowMut;

// submission codes
impl Solution {
    pub fn add_two_numbers(l1: Option<Box<ListNode>>, l2: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
        let (mut l1, mut l2) = (l1, l2);
        let mut sum = 0;
        let mut front = ListNode::new(0);
        let mut current = &mut front;
        loop {
            let mut not_end_count = 0;
            if let Some(node) = l1 {
                sum += node.val;
                not_end_count += 1;
                l1 = node.next;
            }
            if let Some(node) = l2 {
                sum += node.val;
                not_end_count += 1;
                l2 = node.next;
            }
            if not_end_count > 0 || sum > 0 {
                current.next = Some(Box::new(ListNode::new(sum % 10)));
                // current = current.next.as_deref_mut().unwrap(); // leetcode不支持
                current = current.next.as_mut().unwrap().as_mut();
                sum /= 10;
            } else {
                break front.next
            }
        }
    }
}

// submission codes end

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_2() {
        assert_eq!(Solution::add_two_numbers(to_list(vec![2, 4, 3]), to_list(vec![5, 6, 4])), to_list(vec![7, 0, 8]));
        assert_eq!(Solution::add_two_numbers(to_list(vec![1]), to_list(vec![1])), to_list(vec![2]));
        assert_eq!(Solution::add_two_numbers(to_list(vec![9]), to_list(vec![9])), to_list(vec![8, 1]));
        assert_eq!(Solution::add_two_numbers(to_list(vec![9]), to_list(vec![1, 2])), to_list(vec![0, 3]));
        assert_eq!(Solution::add_two_numbers(to_list(vec![0]), to_list(vec![0])), to_list(vec![0]))
    }
}
