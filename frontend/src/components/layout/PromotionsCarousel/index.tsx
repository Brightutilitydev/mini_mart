import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const PromotionsCarousel = () => {
  const settings = {
    infinite: true,
    autoplay: true,
    speed: 500,
    slidesToShow: 2,
    slidesToScroll: 1,
    autoplaySpeed: 3000,
    arrows: false
  };
  return (
    <div className="carousel-list">
      <Slider {...settings}>
        <section className="carousel-item">
          <div className="carousel-image">
            <img src="/dummies/banner-image-2.jpg" alt="" />
          </div>
          <div className="carousel-copy">
            <h2 className="carousel-title">
              <a href="/products/2021">Bananas</a>
            </h2>
            <p className="carousel-p">
              Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere,
              debitis? Earum aliquid porro illo minima ipsum molestias corporis,
              delectus laudantium officia veritatis rem nulla vero dolores totam
              amet, id eum.
            </p>
            <button className="carousel-btn" data-btn>
              Add to Cart
            </button>
          </div>
        </section>

        <section className="carousel-item">
          <div className="carousel-image">
            <img src="/dummies/singel-product-item.jpg" alt="" />
          </div>
          <div className="carousel-copy">
            <h2 className="carousel-title">
              <a href="/products/2021">Bananas</a>
            </h2>
            <p className="carousel-p">
              Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere,
              debitis? Earum aliquid porro illo minima ipsum molestias corporis,
              delectus laudantium officia veritatis rem nulla vero dolores totam
              amet, id eum.
            </p>
            <button className="carousel-btn" data-btn>
              Add to Cart
            </button>
          </div>
        </section>

        <section className="carousel-item">
          <div className="carousel-image">
            <img src="/dummies/post-thumb-1.jpg" alt="" />
          </div>
          <div className="carousel-copy">
            <h2 className="carousel-title">
              <a href="/products/2021">Bananas</a>
            </h2>
            <p className="carousel-p">
              Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere,
              debitis? Earum aliquid porro illo minima ipsum molestias corporis,
              delectus laudantium officia veritatis rem nulla vero dolores totam
              amet, id eum.
            </p>
            <button className="carousel-btn" data-btn>
              Add to Cart
            </button>
          </div>
        </section>

        <section className="carousel-item">
          <div className="carousel-image">
            <img src="/dummies/slide-1.jpg" alt="" />
          </div>
          <div className="carousel-copy">
            <h2 className="carousel-title">
              <a href="/products/2021">Bananas</a>
            </h2>
            <p className="carousel-p">
              Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere,
              debitis? Earum aliquid porro illo minima ipsum molestias corporis,
              delectus laudantium officia veritatis rem nulla vero dolores totam
              amet, id eum.
            </p>
            <button className="carousel-btn" data-btn>
              Add to Cart
            </button>
          </div>
        </section>
      </Slider>
    </div>
  );
};

export default PromotionsCarousel;
