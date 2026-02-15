import { cn } from '@utils/helpers';

export const Card = ({ children, className = '', ...props }) => {
  return (
    <div
      className={cn(
        'bg-white rounded-xl shadow-sm border border-neutral-200/60 transition-shadow duration-300 hover:shadow-md',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader = ({ children, className = '', ...props }) => {
  return (
    <div
      className={cn('p-6 border-b border-neutral-100', className)}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardBody = ({ children, className = '', ...props }) => {
  return (
    <div className={cn('p-6', className)} {...props}>
      {children}
    </div>
  );
};

export const CardFooter = ({ children, className = '', ...props }) => {
  return (
    <div
      className={cn('p-6 border-t border-neutral-100 bg-neutral-50/50', className)}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
