import Prelude hiding (lookup)

data BinaryTree k v = None | Node {
	  key    :: k
	, value  :: v
	, left   :: BinaryTree k v
	, right  :: BinaryTree k v
}

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k None = Nothing
lookup k n |(key n) == k = Just (value n)
		   |(key n) > k = lookup k (left n)
		   |otherwise = lookup k (right n)

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v None = Node k v None None
insert k v n | (key n) == k = Node k v (left n) (right n)
			 | (key n) > k = Node (key n) (value n) (insert k v (left n)) (right n)
			 | otherwise = Node (key n) (value n) (left n) (insert k v (right n))

merge :: Ord k => BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge a None = a
merge None b = b
merge a b = Node (key a) (value a) (left a) (merge (right a) b)

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k None = None
delete k n | (key n) == k = merge (left n) (right n)
		   | (key n) > k = Node (key n) (value n) (delete k (left n)) (right n)
		   | otherwise = Node (key n) (value n) (left n) (delete k (right n)) 
